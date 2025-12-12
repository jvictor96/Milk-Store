from typing import Annotated
from pydantic import BaseModel, Field, model_validator
from dependencies import settings
import datetime

class BatchDTO(BaseModel):
    model_config = {
        "extra": "forbid",
        "json_schema_extra": {
            "example": 
                {
                    "batch_code": "SCH-20251210-1234",
                    "received_at": "2025-12-10T08:30:00Z",
                    "volume_liters": 1000,
                    "fat_percent": 3.5,
                    "shelf_life_days": 30
                }
            
        }}
    batch_code: Annotated[str, Field(pattern=settings.string_patterns.batch_code)]
    received_at: Annotated[str, Field(pattern=settings.string_patterns.received_at)]
    expiry_date: Annotated[str | None, Field(None, pattern=settings.string_patterns.expiry_date)]
    shelf_life_days: int = Field(
        settings.api_parameters.default_batch_shelf_life_days, 
        ge=settings.api_parameters.min_batch_shelf_life_days, 
        le=settings.api_parameters.max_batch_shelf_life_days)
    volume_liters: float = Field(ge=settings.api_parameters.min_batch_volume_liters)
    fat_percent: float = Field(gt=settings.api_parameters.min_batch_fat_percentage)
    available_liters: float | None = Field(None, ge=0)
    deleted_at: Annotated[str | None, Field(None, pattern=settings.string_patterns.deleted_at)]

    def get_shelf_life_days_as_timedelta(self) -> datetime.datetime:
        return datetime.timedelta(days=self.shelf_life_days)

    def get_received_at_as_datetime(self) -> datetime.datetime:
        return datetime.datetime.strptime(self.received_at, settings.datetime_string_formats.received_at)

    def get_batch_code_as_datetime(self) -> datetime.datetime:
        return datetime.datetime.strptime(self.batch_code[4:12], settings.datetime_string_formats.batch_code)
    
    @model_validator(mode='after')
    def check_batch_timestamps(self):
        now = datetime.datetime.now()
        code_date = self.get_batch_code_as_datetime()
        received_at_date = self.get_received_at_as_datetime()
        expiry_date = received_at_date + datetime.timedelta(days=self.shelf_life_days)
        if code_date > now:
            raise ValueError("The code date is a future date")
        if received_at_date > now:
            raise ValueError("The received_at date is a future date")
        if code_date.date() != received_at_date.date():
            raise ValueError("The received_at date and code date diverge")
        if expiry_date < now:
            raise ValueError("The batch is already expired")
        return self