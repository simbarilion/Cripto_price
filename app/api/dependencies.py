from typing import Annotated

from fastapi import Depends, Query
from sqlalchemy.orm import Session

from app.db.database import get_db

DBSession = Annotated[Session, Depends(get_db)]

Ticker = Annotated[str, Query(...)]
Limit = Annotated[int, Query(le=10000)]
Offset = Annotated[int, Query()]

From_ts = Annotated[int, Query(...)]
To_ts = Annotated[int, Query(...)]
