from domain.ports.batch_repository_port import BatchRepositoryPort
from domain.ports.order_repository_port import OrderRepositoryPort
from repositories.in_memory_batches import InMemoryBatches
from repositories.in_memory_orders import InMemoryOrders
from repositories.postgres.batches_adapter import BatchesAdapter
from repositories.postgres.orders_adapter import OrdersAdapter
from config import settings

di_container = {}

di_container["standalone"] = {
    BatchRepositoryPort: InMemoryBatches,
    OrderRepositoryPort: InMemoryOrders
}

di_container["integrated"] = {
    BatchRepositoryPort: BatchesAdapter,
    OrderRepositoryPort: OrdersAdapter
}

env_container = {}

for port, adapter in di_container[settings.environment].items():
    env_container[port] = adapter()