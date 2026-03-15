from pydantic import BaseModel


class PriceResponse(BaseModel):
    """Pydantic модель для возврата данных о ценах валют"""

    price: float
    timestamp: int

    class Config:
        orm_mode = True  # FastAPI автоматически конвертировать объекты SQLAlchemy в Pydantic
