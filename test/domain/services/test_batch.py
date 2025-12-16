import pytest

from domain.service.batch_service import BatchService
from repositories.in_memory.batches import InMemoryBatches
from repositories.in_memory.orders import InMemoryOrders

service = BatchService(InMemoryBatches(), InMemoryOrders())

def test_pytest():
    assert 1 == 1