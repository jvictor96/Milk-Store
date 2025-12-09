from abc import ABC, abstractmethod
import datetime
from domain.schemas.batch_post_payload import BatchPostPayload
from domain.schemas.batch_database_entry import BatchDatabaseEntry

class BatchRepository(ABC):
    @abstractmethod
    def get_batch_by_id(self, id: str) -> BatchDatabaseEntry:
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

# TODO: implement available_liters = volume_liters - sum(consumed) filter
class HardCodedBatches(BatchRepository):

    batches: dict[str, BatchDatabaseEntry] = {
        "SCH-20251208-0001": BatchDatabaseEntry.build(BatchPostPayload.build("SCH-20251208-0001", "2025-12-08T08:30:00Z")), 
        "SCH-20251205-0001": BatchDatabaseEntry.build(BatchPostPayload.build("SCH-20251205-0001", "2025-12-05T08:30:00Z")), 
        "SCH-20251205-0002": BatchDatabaseEntry.build(BatchPostPayload.build("SCH-20251205-0002", "2025-12-05T08:30:00Z")), 
        "SCH-20251207-0001": BatchDatabaseEntry.build(BatchPostPayload.build("SCH-20251207-0001", "2025-12-07T08:30:00Z"))
    }
    
    def get_batch_by_id(self, id: str) -> BatchDatabaseEntry:
        return [batch for batch in self.batches if batch.batch_code == id]
    
    def get_active_batches_until_date(self, date: datetime.datetime) -> list[BatchDatabaseEntry]:
        return [batch for batch in self.batches if batch.expiry_date > date]
    
    def post_batch(self, batch: BatchDatabaseEntry) -> BatchDatabaseEntry:
        self.batches[batch.batch_code] = batch

    def update_batch(self, batch: BatchDatabaseEntry) -> BatchDatabaseEntry:
        self.batches[batch.batch_code] = batch

    def delete_batch(self, batch: str):
        self.batches[batch.batch_code].deleted_at = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")