from typing import Annotated
from pydantic import BaseModel, Field
import datetime

class OrderPostPayload(BaseModel):
    qty: int = Field(7, ge=1)
    order_id: Annotated[str | None, Field(pattern='^ORDER-\\d{8}-\\d{4}$')]

def check_order_timestamps(consume: OrderPostPayload):
    now = datetime.datetime.now()
    code_date = datetime.datetime.strptime(consume.order_id[6:14],"%Y%m%d")
    if code_date > now:
        raise ValueError("The code date is a future date")
    return consume