from typing import Annotated
from pydantic import BaseModel, Field, model_validator
import datetime
from dependencies import settings

class OrderDto(BaseModel):
    model_config = {
        "extra": "forbid",
        "json_schema_extra": {
            "example": 
                {
                    "order_id": "ORDER-20251210-1234",
                    "qty": 100
                }
            
        }}
    qty: float = Field(7, ge=1)
    order_id: Annotated[str | None, Field(pattern='^ORDER-\\d{8}-\\d{4}$')]
    batch_code: Annotated[str | None, Field(None, pattern='^SCH-\\d{8}-\\d{4}$')]

    def get_order_id_as_datetime(self) -> datetime.datetime:
        return datetime.datetime.strptime(self.order_id[6:14], settings.datetime_string_formats.order_id)

    def get_batch_code_as_datetime(self) -> datetime.datetime:
        return datetime.datetime.strptime(self.batch_code[4:12], settings.datetime_string_formats.batch_code)
    
    @model_validator(mode='after')
    def check_order_timestamps(self):
        now = datetime.datetime.now()
        code_date = datetime.datetime.strptime(self.order_id[6:14],"%Y%m%d")
        if code_date > now:
            raise ValueError("The code date is a future date")
        return self