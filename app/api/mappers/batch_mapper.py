from api.schemas.batch_dto import BatchDTO
from domain.schemas.batch import Batch
from dependencies import settings


class BatchMapper():
    @staticmethod
    def to_domain(batch: BatchDTO) -> Batch:
        return Batch(
            batch.batch_code, 
            batch.get_received_at_as_datetime(), 
            batch.volume_liters, 
            batch.fat_percent, 
            batch.get_shelf_life_days_as_timedelta()
            )
    
    @staticmethod
    def to_dto(batch: Batch) -> BatchDTO:
        return BatchDTO(
            batch_code=batch.batch_code,
            received_at=batch.received_at.strftime(settings.datetime_string_formats.received_at),
            shelf_life_days=batch.calculate_shelf_life_days(),
            volume_liters=batch.volume_liters,
            fat_percent=batch.fat_percent,
            available_liters=batch.volume_liters - batch.consumed,
            deleted_at = batch.deleted_at
        )