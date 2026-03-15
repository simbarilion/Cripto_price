## CriptoPrice

Сервис для периодического получения индексов цен криптовалют с биржи Deribit и сохранения их в базу данных PostgreSQL.  
Данные предоставляются через REST API, реализованное на FastAPI.

## Функциональность

Сервис выполняет следующие задачи:

- Каждую минуту получает индексную цену валют **BTC/USD** и **ETH/USD** с API биржи Deribit
- Сохраняет тикер, цену, и время в формате **UNIX timestamp** в PostgreSQL
- Предоставляет REST API для получения сохранённых данных
- Поддерживает пагинацию для запросов истории цен

Поддерживаемые тикеры: btc_usd, eth_usd

## Технологии

- **Python 3.12**
- **FastAPI**
- **PostgreSQL**
- **SQLAlchemy**
- **Celery**
- **Redis**
- **aiohttp** (асинхронный HTTP-клиент)

## Архитектура

API Layer (FastAPI) -> Service Layer + Celery Worker -> Database (PostgreSQL)

## Структура проекта

    app/
    │
    ├── api/ # FastAPI endpoints
    ├── db/ # модели БД и подключение
    ├── schemas/ # Pydantic схемы
    ├── services/ # бизнес-логика
    ├── tasks/ # Celery задачи
    ├── core/ # конфигурация и логирование
    ├── tests/ # тестирование бизнес-логики
    ├── main.py # точка входа приложения
    │
    .env.example # пример настройки перменных окружения
    │
    Makefile # запуск линтеров и форматирования
    │
    .pre-commit-config.yaml # проверка линтерами перед коммитом

**main.py** — точка входа приложения. Отвечает за инициализацию FastAPI, подключение роутеров, middleware, 
зависимостей и запуск сервера.

## API

### Получение всех данных по валюте

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

### Получение последней цены валюты

**GET /price/latest?ticker=btc_usd**

Если данных нет — возвращается 404 Not Found.

Пример ответа:
```
{
  "price": 71766.86,
  "timestamp": 1773608280
}
```

### Получение цены валюты за период

**GET /price/by-date?ticker=btc_usd&from_ts=1773608340&to_ts=1773608400**

Возвращает список цен в указанном диапазоне времени

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

## Установка и локальный запуск

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
4. Заполните Redis
```
redis-server
```
5. Запустите Celery worker
```
celery -A app.tasks.celery_app worker -l info

# для Windows используйте
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

- Реализованы unit-тесты и асинхронные тесты (pytest + pytest_asyncio)

**Покрытие тестами:** 59%

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

- **Celery** - для периодического выполнения фоновых задач (получения цен каждую минуту).

- **aiohttp** - асинхронный HTTP-клиент для параллельного получения цен.

- **Service Layer** - бизнес-логика вынесена из контроллеров API в сервисный слой для удобства тестирования и читаемости.

- **PostgreSQL** - для хранения истории цен с индексами для быстрого поиска.

- **Pre-commit** - автоматический запуск линтеров перед коммитом.

## Возможные улучшения

- Docker контейнеризация (FastAPI, Celery, Redis, PostgreSQL)
- Ограничение частоты запросов (rate limiting)
- Кэширование последних цен
- Поддержка дополнительных тикеров
- Alembic для управления миграциями базы данных в продакшене
