import datetime
from domain.schemas.batch import Batch
from domain.ports.batch_repository_port import BatchRepositoryPort
from typing import Optional
from dependencies import settings

class InMemoryBatches(BatchRepositoryPort):

    batches: dict[str, Batch] = {
        "SCH-20251208-0001": Batch(
            "SCH-20251208-0001", 
            datetime.datetime.strptime("2025-12-08T08:30:00Z", settings.datetime_string_formats.received_at),
            1000,
            3.5,
            datetime.timedelta(days=5)
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

    def update_batch(self, batch: Batch) -> Batch:
        self.batches[batch.batch_code] = batch

    def delete_batch(self, batch_code: str):
        self.batches[batch_code].deleted_at = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")