from typing import Annotated
from pydantic import BaseModel, Field
import datetime


class BatchGetResponse(BaseModel):
    model_config = {"extra": "forbid"}
    batch_code: Annotated[str, Field(pattern='^SCH-\\d{8}-\\d{4}$')]
    received_at: Annotated[str, Field(pattern='^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}Z$')]
    shelf_life_days: int = Field(7, ge=1, le=30)
    volume_liters: float = Field(gt=0)
    fat_percent: float = Field(gt=0)
    available_liters: float = Field(ge=0)   # TODO: implement available_liters = volume_liters - sum(consumed)