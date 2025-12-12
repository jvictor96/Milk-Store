from pydantic_settings import SettingsConfigDict
from pydantic import BaseModel
from yaml_settings_pydantic import BaseYamlSettings

class StringPatternSettings(BaseModel):
    batch_code: str
    order_id: str
    received_at: str
    deleted_at: str
    expiry_date: str

class DatetimeStringFormats(BaseModel):
    batch_code: str
    order_id: str
    received_at: str
    deleted_at: str
    expiry_date: str

class ApiParametersSettings(BaseModel):
    max_batch_shelf_life_days: int
    min_batch_shelf_life_days: int
    default_batch_shelf_life_days: int
    min_batch_volume_liters: float
    min_batch_fat_percentage: float
    min_order_volume_liters: float

class Settings(BaseYamlSettings):
    string_patterns: StringPatternSettings
    api_parameters: ApiParametersSettings
    datetime_string_formats: DatetimeStringFormats

    model_config = SettingsConfigDict(
        yaml_files = "./properties.yaml"
    )

settings = Settings()