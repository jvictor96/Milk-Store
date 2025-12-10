from typing import Annotated
from pydantic import BaseModel, Field

from domain.schemas.order_post_payload import OrderPostPayload

class OrderDatabaseEntry(BaseModel):
    qty: int = Field(7, ge=1)
    order_id: Annotated[str | None, Field(pattern='^ORDER-\\d{8}-\\d{4}$')]
    batch_id: Annotated[str | None, Field(pattern='^SCH-\\d{8}-\\d{4}$')]

    @staticmethod
    def build(order: OrderPostPayload, batch_id: str):
        return OrderDatabaseEntry(**{
            "qty" : order.qty,
            "order_id" : order.order_id,     # TODO: define order_id if it's absent
            "batch_id" : batch_id
        })