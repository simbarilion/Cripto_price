## CriptoPrice

Сервис для периодического получения индексов цен криптовалют с биржи Deribit и сохранения их в базу данных PostgreSQL.  
Данные предоставляются через REST API, реализованное на FastAPI.

## Функциональность

Сервис выполняет следующие задачи:

- Каждую минуту получает индексную цену валют **BTC/USD** и **ETH/USD** с API биржи Deribit
- Сохраняет цену, тикер и время в формате **UNIX timestamp** в PostgreSQL
- Предоставляет REST API для получения сохранённых данных

## Технологии

- **Python**
- **FastAPI**
- **PostgreSQL**
- **SQLAlchemy**
- **Celery**
- **Redis**
- **aiohttp**

## Архитектура

API Layer (FastAPI) -> Service Layer + Celery Worker -> Database

## Структура проекта

    app/
    │
    ├── api/ # FastAPI endpoints
    ├── db/ # модели БД и подключение
    ├── schemas/ # Pydantic схемы
    ├── services/ # бизнес-логика
    ├── tasks/ # Celery задачи
    ├── core/ # конфигурация и логирование

## API

### Получение всех данных по валюте

GET /prices?ticker=btc_usd

Дополнительно поддерживается пагинация:

GET /prices?ticker=btc_usd&limit=100&offset=0

### Получение последней цены валюты

GET /price/latest?ticker=btc_usd

Если данных нет — возвращается **404**.

### Получение цены валюты за период

GET /price/by-date?ticker=btc_usd&from_ts=1700000000&to_ts=1700100000

Возвращает список цен в указанном диапазоне времени

## Установка и локальный запуск

1. Клонируйте репозиторий
````
git clone https://gitlab.com/simbarilion/Cripto_price.git
cd Cripto_price
````
2. Установите зависимости
````
pip install -r requirements.txt
или
poetry install
````
3. Заполните .env
````
DEBUG=True

DATABASE_URL=postgresql://postgres:password@localhost:5432/crypto_deribit

LOCATION=redis://127.0.0.1:6379/0
CELERY_BROKER_URL=redis://127.0.0.1:6379/1
CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/2
````
4. Заполните Redis
````
redis-server
````
5. Запустите Celery worker
````
celery -A app.tasks.celery_app worker -l info
или
celery -A app.tasks.celery_app worker -l info -P solo
````
6. Запустите Celery beat
````
celery -A app.tasks.celery_app beat -l info
````
7. Запустите FastAPI
````
uvicorn app.main:app --reload
````
API будет доступно:

http://localhost:8000/docs

### Тестирование

- Реализованы unit-тесты

**Покрытие тестами:** 60%

**Запуск тестов:**
```bash

pytest
```
Запустить тесты с выводом покрытия в терминал:
```
pytest --cov=. --cov-report=term-missing
```
Сформировать HTML-отчёт о покрытии (папка htmlcov/):
```
pytest --cov=. --cov-report=html
```

## Архитектурные решения (Design decisions)

- **Celery**. Используется для периодического выполнения фоновых задач — получения цен с биржи каждую минуту.

- **aiohttp**. Асинхронный HTTP-клиент позволяет одновременно получать цены нескольких валют.

- **Service Layer**. Бизнес-логика вынесена из API-контроллеров в сервисный слой для улучшения читаемости и тестируемости кода.

- **PostgreSQL**. Используется для хранения истории цен благодаря надёжности и хорошей поддержке индексов.

## Возможные улучшения

- Docker контейнеризация
- Ограничение частоты запросов (rate limiting)
- Кэширование последних цен
