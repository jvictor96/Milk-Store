from pydantic_settings import SettingsConfigDict
from pydantic import BaseModel
from yaml_settings_pydantic import BaseYamlSettings

class ExampleSettings(BaseModel):
    batch_code: str
    batch_code_to_delete_during_tests: str
    batch_code_to_create_during_tests: str
    batch_code_to_test_near_expiry: str
    order_id: str
    received_at: str
    deleted_at: str
    expiry_date: str
    volume_liters: float
    fat_percent: float
    shelf_life_days: int
    qty: float

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

class DatabaseConnectionSettings(BaseModel):
    user: str
    password: str
    host: str
    port: int
    name: str

class Settings(BaseYamlSettings):
    environment: str
    string_patterns: StringPatternSettings
    api_parameters: ApiParametersSettings
    datetime_string_formats: DatetimeStringFormats
    examples: ExampleSettings
    database_connection: DatabaseConnectionSettings

    model_config = SettingsConfigDict(
        yaml_files = "./properties.yaml",
        env_nested_delimiter="__"
    )

settings = Settings()