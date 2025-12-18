import datetime
from domain.schemas.batch import Batch
from domain.ports.batch_repository_port import BatchRepositoryPort
from typing import Optional
from config import settings

class InMemoryBatches(BatchRepositoryPort):

    batches: dict[str, Batch] = {
        settings.examples.batch_code: Batch(
            settings.examples.batch_code, 
            datetime.datetime.strptime(settings.examples.received_at, settings.datetime_string_formats.received_at),
            settings.examples.volume_liters,
            settings.examples.fat_percent,
            datetime.timedelta(days=settings.examples.shelf_life_days)
        ), 
        settings.examples.batch_code_to_delete_during_tests: Batch(
            settings.examples.batch_code_to_delete_during_tests, 
            datetime.datetime.strptime(settings.examples.received_at, settings.datetime_string_formats.received_at),
            settings.examples.volume_liters,
            settings.examples.fat_percent,
            datetime.timedelta(days=settings.examples.shelf_life_days)
        ), 
    }
    
    def get_batch_by_id(self, id: str) -> Optional[Batch]:
        return self.batches[id] if id in self.batches else None
    
    def get_active_batches(self) -> list[Batch]:
        return [self.batches[batch] for batch in self.batches if 
                self.batches[batch].expiry_date > datetime.datetime.now() and
                self.batches[batch].deleted_at == None and 
                self.batches[batch].consumed < self.batches[batch].volume_liters]
    
    def get_active_batches_until_date(self, date: datetime.datetime) -> list[Batch]:
        return [self.batches[batch] for batch in self.batches if 
                self.batches[batch].expiry_date > datetime.datetime.now() and 
                self.batches[batch].expiry_date < date and 
                self.batches[batch].deleted_at == None and 
                self.batches[batch].consumed < self.batches[batch].volume_liters]
    
    def post_batch(self, batch: Batch) -> Batch:
        self.batches[batch.batch_code] = batch

    def update_batch(self, batch_id: str, batch: Batch) -> Batch:
        self.batches[batch_id] = batch