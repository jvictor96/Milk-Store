from typing import Annotated
from pydantic import BaseModel, Field
import datetime

class BatchGetResponse(BaseModel):
    model_config = {"extra": "forbid"}
    batch_code: Annotated[str, Field(pattern='^SCH-\\d{8}-\\d{4}$')]
    received_at: Annotated[str, Field(pattern='^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}Z$')]
    shelf_life_days: int = Field(7, ge=1, le=30)   # documentation says "shelf-life typically ranges from 7 to 30 days"
    volume_liters: float = Field(gt=0)
    fat_percent: float = Field(gt=0)
    available_liters: float = Field(ge=0)   # TODO: implement available_liters = volume_liters - sum(consumed)

    def __init__(self, 
                batch_code: str, 
                received_at: str, 
                volume_liters: int = 1000, 
                fat_percent:float = 3.5, 
                shelf_life_days:int = 7):
        self.batch_code = batch_code
        self.received_at = received_at
        self.shelf_life_days = shelf_life_days
        self.volume_liters = volume_liters
        self.fat_percent = fat_percent