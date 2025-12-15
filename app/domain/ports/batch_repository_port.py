from abc import ABC, abstractmethod
import datetime
from domain.schemas.batch import Batch
from typing import Optional

# TODO: Implement Postgres connection
class BatchRepositoryPort(ABC):
    @abstractmethod
    def get_batch_by_id(self, id: str) -> Optional[Batch]:
        pass
    @abstractmethod
    def get_active_batches(self) -> list[Batch]:
        pass
    @abstractmethod
    def get_active_batches_until_date(self, date: datetime.datetime) -> list[Batch]:
        pass
    @abstractmethod
    def post_batch(self, batch: Batch) -> Batch:
        pass
    @abstractmethod
    def update_batch(self, batch: Batch) -> Batch:
        pass