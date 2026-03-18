## CriptoPrice

Сервис для периодического получения индексов цен криптовалют с биржи Deribit и сохранения их в базу данных PostgreSQL.  
Данные доступны через REST API, реализованное на FastAPI.

## Функциональность

Сервис состоит из двух частей:
- API сервер — предоставляет доступ к сохранённым данным
- Celery worker — выполняет фоновые задачи получения цен

Сервис выполняет следующие задачи:

- Каждую минуту получает индексные цены валют **BTC/USD** и **ETH/USD** с API биржи Deribit
- Сохраняет тикер, цену, и время в формате **UNIX timestamp** в PostgreSQL
- Хранит историю цен в PostgreSQL
- Предоставляет REST API для получения данных
- Поддерживает пагинацию и фильтрацию по дате
- Выполняет асинхронные HTTP запросы для ускорения получения данных

Поддерживаемые тикеры: 
- btc_usd 
- eth_usd

## Технологии

- **Python 3.12**
- **FastAPI**
- **PostgreSQL**
- **SQLAlchemy 2**
- **Celery**
- **Redis**
- **aiohttp** (асинхронный HTTP-клиент)
- **pytest**

## Архитектура
Сервис использует слоистую архитектуру.
    FastAPI API
          │
          ▼
    Service Layer
          │
          ▼
    Repository Layer
          │
          ▼
    PostgreSQL

Фоновая обработка данных:
    Celery Worker
          │
          ▼
    Async Deribit Client (aiohttp)
          │
          ▼
    PostgreSQL


## Структура проекта

    app/
    │
    ├── api/                   # FastAPI endpoints
    │   ├── routes.py
    │   ├── health.py
    │   └── dependencies.py
    ├── db/                    # модели БД и подключение
    │   ├── database.py
    │   └── models.py
    │
    ├── schemas/               # Pydantic схемы
    │
    ├── services/              # бизнес-логика
    │   ├── deribit_client.py
    │   ├── price_fetcher.py
    │   └── price_service.py
    │
    ├── tasks/                 # Celery задачи
    │   ├── celery_app.py
    │   └── price_tasks.py
    │
    ├── core/                  # middleware, логирование, конфигурация
    │
    ├── tests/                 # тестирование бизнес-логики
    │
    ├── main.py                # точка входа приложения
    │
    .env.example               # пример настройки перменных окружения
    │
    Makefile                   # запуск линтеров и форматирования
    │
    .pre-commit-config.yaml    # проверка линтерами перед коммитом

**main.py** — точка входа приложения. Отвечает за инициализацию FastAPI, подключение роутеров, middleware, 
зависимостей и запуск сервера.

## API

Документация доступна после запуска:

```
http://localhost:8000/docs
```

### Получение истории цен

**GET /prices**

Пример запроса:

**GET /prices?ticker=btc_usd&limit=2&offset=0**

Параметры:

- ticker — тикер валюты (обязательный)

- limit — количество записей (по умолчанию 100, максимум 1000)

- offset — смещение для пагинации (по умолчанию 0)

Пример ответа:
```
[
  {
    "price": 71772.03,
    "timestamp": 1773608220
  },
  {
    "price": 71741.7,
    "timestamp": 1773608160
  }
]
```

### Получение последней цены

**GET /prices/latest**

Пример запроса:

**GET /price/latest?ticker=btc_usd**

Пример ответа:
```
{
  "price": 71766.86,
  "timestamp": 1773608280
}
```
Если данных нет — возвращается 404 Not Found.

### Получение цен за период

**GET /prices/by-date**

Пример запроса:

**GET /price/by-date?ticker=btc_usd&from_ts=1773608340&to_ts=1773608400**

Параметры:

- from_ts — начало периода (UNIX timestamp)

- to_ts — конец периода (UNIX timestamp)

Пример ответа:
```
[
  {
    "price": 71763.8,
    "timestamp": 1773608340
  },
  {
    "price": 71741.98,
    "timestamp": 1773608400
  }
]
```

### Health checks

Проверка состояния сервиса:

**GET /health**

Проверка соединения с базой данных:

**GET /health/db**

## Установка и запуск

1. Клонируйте репозиторий:
```
git clone https://gitlab.com/simbarilion/Cripto_price.git
cd Cripto_price
```
2. Установите зависимости:
```
pip install -r requirements.txt
или
poetry install
```
3. Настройте переменные окружения в .env:
```
DEBUG=True

# PostgreSQL
DATABASE_URL=postgresql://postgres:password@localhost:5432/crypto_deribit

# Redis / Celery
LOCATION=redis://127.0.0.1:6379/0
CELERY_BROKER_URL=redis://127.0.0.1:6379/1
CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/2
```
4. Запустите Redis
```
redis-server
```
5. Запустите Celery worker
```
# Linux / Mac:

celery -A app.tasks.celery_app worker -l info

# Windows:

celery -A app.tasks.celery_app worker -l info -P solo
```
6. Запустите Celery beat
```
celery -A app.tasks.celery_app beat -l info
```
7. Запустите FastAPI
```
uvicorn app.main:app --reload
```
API будет доступно по адресу:

http://localhost:8000/docs

### Тестирование

Используются:

- pytest
- pytest-asyncio

**Покрытие тестами:** 65%

**Запуск тестов:**
```bash

pytest
```
Запустить тесты с покрытием в терминал:
```
pytest --cov=. --cov-report=term-missing
```
HTML-отчёт о покрытии:
```
pytest --cov=. --cov-report=html
```

## Архитектурные решения (Design decisions)

- **Celery**
  - Используется для выполнения периодических фоновых задач
  - Celery Beat запускает задачу получения цен каждую минуту

- **aiohttp**
  - Асинхронный HTTP клиент используется для параллельного получения цен
  - Это значительно ускоряет сбор данных

- **Service Layer**
  - Бизнес-логика вынесена из API контроллеров в отдельный сервисный слой.
  - Преимущества:
    - проще тестировать
    - легче поддерживать
    - разделение ответственности

- **Repository Layer**
  - SQL запросы изолированы в отдельном слое.
  - Это позволяет:
    - легко изменять способ хранения данных
    - упрощает тестирование

- **PostgreSQL**
- Используются индексы: ticker, timestamp, idx_ticker_timestamp
- Это ускоряет:
  - поиск последней цены
  - фильтрацию по периоду
  - фильтрацию по нескольким полям (ticker, timestamp)

- Middleware
  - Используется для логирования HTTP запросов и времени выполнения

- **Pre-commit**
  - Перед каждым коммитом автоматически запускаются:
    - линтеры
    - форматирование

## Возможные улучшения

- Docker контейнеризация
- Ограничение частоты запросов (rate limiting)
- Кэширование последних цен
- Поддержка дополнительных криптовалют
- Alembic миграции

## Автор

Надежда Попова

Python Developer

📧 nadezhdapopova13@yandex.ru

🔗 GitHub: simbarilion
