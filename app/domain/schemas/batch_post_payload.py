from typing import Annotated
from pydantic import BaseModel, Field
import datetime

class BatchPostPayload(BaseModel):
    model_config = {"extra": "forbid"}
    batch_code: Annotated[str, Field(pattern='^SCH-\\d{8}-\\d{4}$')]
    received_at: Annotated[str, Field(pattern='^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}Z$')]
    shelf_life_days: int = Field(7, ge=1, le=30)   # documentation says "shelf-life typically ranges from 7 to 30 days"
    volume_liters: float = Field(gt=0)
    fat_percent: float = Field(gt=0)

    @staticmethod
    def build(  batch_code: str, 
                received_at: str, 
                volume_liters: int = 1000, 
                fat_percent:float = 3.5, 
                shelf_life_days:int = 7):
        return BatchPostPayload(**{
            "batch_code" : batch_code,
            "received_at" : received_at,
            "shelf_life_days" : shelf_life_days,
            "volume_liters" : volume_liters,
            "fat_percent" : fat_percent
        })

def check_timestamps(batch: BatchPostPayload):
    now = datetime.datetime.now()
    code_date = datetime.datetime.strptime(batch.batch_code[4:12],"%Y%m%d")
    received_at_date = datetime.datetime.strptime(batch.received_at,"%Y-%m-%dT%H:%M:%SZ")
    # expiry_date = received_at_date + datetime.timedelta(days=batch.shelf_life_days)
    # if code_date > now:
    #     raise ValueError("The code date is a future date")
    # if received_at_date > now:
    #     raise ValueError("The received_at date is a future date")
    # if code_date.date() != received_at_date.date():
    #     raise ValueError("The received_at date and code date diverge")
    # if expiry_date < now:
    #     raise ValueError("The batch is already expired")