from pydantic import BaseModel, Field


class PriceResponse(BaseModel):
    """Pydantic модель для возврата данных о ценах валют"""

    price: float = Field(gt=0)
    timestamp: int = Field(ge=0)

    model_config = {
        "from_attributes": True,
        "extra": "forbid",
        "strict": True,
        "validate_assignment": True,
    }
