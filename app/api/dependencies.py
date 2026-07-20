from typing import Annotated, Literal

from fastapi import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db

DBSession = Annotated[AsyncSession, Depends(get_db)]

Ticker = Annotated[Literal["btc_usd", "eth_usd"], Query(...)]
Limit = Annotated[int, Query(le=10000)]
Offset = Annotated[int, Query()]

From_ts = Annotated[int, Query(..., ge=0)]
To_ts = Annotated[int, Query(..., ge=0)]
