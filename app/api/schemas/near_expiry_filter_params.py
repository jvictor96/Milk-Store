from pydantic import BaseModel, Field

class NearExpiryFilterParams(BaseModel):
    n_days: int = Field(7, ge=1)
