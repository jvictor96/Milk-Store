from repositories.schemas.batch_entity import BatchEntity
from domain.schemas.batch import Batch
from dependencies import settings


class BatchMapper():
    @staticmethod
    def to_domain(batch: BatchEntity) -> Batch:
        return Batch(
            batch.batch_code,
            batch.received_at, 
            batch.volume_liters, 
            batch.fat_percent, 
            batch.expiry_date - batch.received_at
            )
    
    @staticmethod
    def to_entity(batch: Batch) -> BatchEntity:
        return BatchEntity(
            batch_code=batch.batch_code,
            received_at=batch.received_at.strftime(settings.datetime_string_formats.received_at),
            expiry_date=batch.expiry_date.strftime(settings.datetime_string_formats.expiry_date),
            volume_liters=batch.volume_liters,
            fat_percent=batch.fat_percent,
            available_liters=batch.volume_liters - batch.consumed,
            deleted_at = batch.deleted_at
        )