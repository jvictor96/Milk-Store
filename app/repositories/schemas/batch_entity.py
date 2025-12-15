import datetime
from sqlmodel import Field, SQLModel
from typing import Annotated
from config import settings

class BatchEntity(SQLModel, table=True):
    batch_code: str = Field(regex=settings.string_patterns.batch_code, primary_key=True)
    received_at: datetime.datetime
    expiry_date: datetime.datetime
    volume_liters: float = Field(ge=settings.api_parameters.min_batch_volume_liters)
    fat_percent: float = Field(gt=settings.api_parameters.min_batch_fat_percentage)
    consumed: float | None = Field(None, ge=0)
    deleted_at: datetime.datetime | None