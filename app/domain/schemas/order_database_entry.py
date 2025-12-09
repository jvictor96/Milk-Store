from typing import Annotated
from pydantic import BaseModel, Field

class OrderDatabaseEntry(BaseModel):
    qty: int = Field(7, ge=1)
    order_id: Annotated[str | None, Field(pattern='^ORDER-\\d{8}-\\d{4}$')]
    batch_id: Annotated[str | None, Field(pattern='^SCH-\\d{8}-\\d{4}$')]