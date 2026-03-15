from pydantic import BaseModel


class PriceResponse(BaseModel):
    """Pydantic модель для возврата данных о ценах валют"""

    price: float
    timestamp: int

    model_config = {"from_attributes": True}  # FastAPI автоматически конвертировать объекты SQLAlchemy в Pydantic
