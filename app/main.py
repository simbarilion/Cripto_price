import uvicorn
from fastapi import FastAPI

from app.api.health import health_router
from app.api.routes import router
from app.core.middleware import log_requests

app = FastAPI(title="Crypto Prices API")

app.middleware("http")(log_requests)

app.include_router(router)
app.include_router(health_router)


if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)
