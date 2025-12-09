from abc import ABC, abstractmethod
import datetime
from app.domain.schemas.order_database_entry import OrderDatabaseEntry
from app.domain.schemas.order_post_payload import OrderPostPayload

class OrderRepository(ABC):
    @abstractmethod
    def post_order(self, batch: OrderPostPayload) -> OrderPostPayload:
        pass

class HardCodedBatches(OrderRepository):

    orders: dict[str, OrderDatabaseEntry] = {}
    
    def post_order(self, order: OrderDatabaseEntry) -> OrderDatabaseEntry:
        self.orders[order.order_id] = order