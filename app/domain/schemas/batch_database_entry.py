from typing import Annotated
from pydantic import BaseModel, Field
from .batch_post_payload import BatchPostPayload
import datetime

class BatchDatabaseEntry(BaseModel):
    model_config = {"extra": "forbid"}
    batch_code: Annotated[str, Field(pattern='^SCH-\\d{8}-\\d{4}$')]
    received_at: Annotated[str, Field(pattern='^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}Z$')]
    expiry_date: datetime.datetime 
    volume_liters: float = Field(gt=0)
    fat_percent: float = Field(gt=0)
    consumed: int = Field(ge=0)
    deleted_at: Annotated[str | None, Field(pattern='^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}Z$')]

    @staticmethod
    def build(batch: BatchPostPayload):
        received_at_date = datetime.datetime.strptime(batch.received_at,"%Y-%m-%dT%H:%M:%SZ")
        return BatchDatabaseEntry(**{
            "expiry_date" : received_at_date + datetime.timedelta(days=batch.shelf_life_days),
            "batch_code" : batch.batch_code,
            "received_at" : batch.received_at,
            "volume_liters" : batch.volume_liters,
            "consumed" : 0,
            "fat_percent" : batch.fat_percent,
            "deleted_at": None
        })
        