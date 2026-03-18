import uvicorn
from fastapi import FastAPI

from app.api.routes import router
from app.core.middleware import log_requests

app = FastAPI(title="Crypto Prices API")

app.include_router(router)

app.middleware("http")(log_requests)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
