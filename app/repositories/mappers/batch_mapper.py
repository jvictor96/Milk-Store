from repositories.schemas.batch_entity import BatchEntity
from domain.schemas.batch import Batch
from config import settings


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
            received_at=batch.received_at,
            expiry_date=batch.expiry_date,
            volume_liters=batch.volume_liters,
            fat_percent=batch.fat_percent,
            consumed=batch.consumed,
            deleted_at = batch.deleted_at
        )
    
    def merge(batch_entity: BatchEntity, batch: Batch) -> BatchEntity:
        batch_entity.received_at = batch.received_at
        batch_entity.consumed = batch.consumed
        batch_entity.expiry_date = batch.expiry_date
        batch_entity.deleted_at = batch.deleted_at
        batch_entity.volume_liters = batch.volume_liters
        batch_entity.fat_percent = batch.fat_percent
        return batch_entity