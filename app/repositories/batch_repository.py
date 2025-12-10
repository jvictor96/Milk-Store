from abc import ABC, abstractmethod
import datetime
from domain.schemas.batch_post_payload import BatchPostPayload
from domain.schemas.batch_database_entry import BatchDatabaseEntry
from typing import Optional

# Implement Postgres connection
class BatchRepository(ABC):
    @abstractmethod
    def get_batch_by_id(self, id: str) -> BatchDatabaseEntry:
        pass
    @abstractmethod
    def get_active_batches(self) -> list[BatchDatabaseEntry]:
        pass
    @abstractmethod
    def get_active_batches_until_date(self, date: datetime.datetime) -> list[BatchDatabaseEntry]:
        pass
    @abstractmethod
    def post_batch(self, batch: BatchDatabaseEntry) -> BatchDatabaseEntry:
        pass
    @abstractmethod
    def update_batch(self, batch: BatchDatabaseEntry) -> BatchDatabaseEntry:
        pass
    @abstractmethod
    def delete_batch(self, id: str):
        pass

class HardCodedBatches(BatchRepository):

    batches: dict[str, BatchDatabaseEntry] = {
        "SCH-20251208-0001": BatchDatabaseEntry.build(BatchPostPayload.build("SCH-20251208-0001", "2025-12-08T08:30:00Z")), 
        "SCH-20251205-0001": BatchDatabaseEntry.build(BatchPostPayload.build("SCH-20251205-0001", "2025-12-05T08:30:00Z")), 
        "SCH-20251205-0002": BatchDatabaseEntry.build(BatchPostPayload.build("SCH-20251205-0002", "2025-12-05T08:30:00Z")), 
        "SCH-20251105-0001": BatchDatabaseEntry.build(BatchPostPayload.build("SCH-20251105-0001", "2025-11-05T08:30:00Z")), 
        "SCH-20251207-0001": BatchDatabaseEntry.build(BatchPostPayload.build("SCH-20251207-0001", "2025-12-07T08:30:00Z"))
    }
    
    def get_batch_by_id(self, id: str) -> Optional[BatchDatabaseEntry]:
        return self.batches[id] if id in self.batches else None
    
    def get_active_batches(self) -> list[BatchDatabaseEntry]:
        return [self.batches[batch] for batch in self.batches if 
                self.batches[batch].expiry_date > datetime.datetime.now() and
                self.batches[batch].deleted_at == None and 
                self.batches[batch].consumed < self.batches[batch].volume_liters]
    
    def get_active_batches_until_date(self, date: datetime.datetime) -> list[BatchDatabaseEntry]:
        return [self.batches[batch] for batch in self.batches if 
                self.batches[batch].expiry_date > datetime.datetime.now() and 
                self.batches[batch].expiry_date < date and 
                self.batches[batch].deleted_at == None and 
                self.batches[batch].consumed < self.batches[batch].volume_liters]
    
    def post_batch(self, batch: BatchDatabaseEntry) -> BatchDatabaseEntry:
        self.batches[batch.batch_code] = batch

    def update_batch(self, batch: BatchDatabaseEntry) -> BatchDatabaseEntry:
        self.batches[batch.batch_code] = batch

    def delete_batch(self, batch_code: str):
        self.batches[batch_code].deleted_at = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")