from abc import ABC, abstractmethod
import datetime
from typing import Optional
from domain.schemas.order_database_entry import OrderDatabaseEntry
from domain.schemas.order_post_payload import OrderPostPayload

class OrderRepository(ABC):
    @abstractmethod
    def post_order(self, batch: OrderPostPayload) -> OrderPostPayload:
        pass
    @abstractmethod
    def get_order_by_id(self, batch: OrderPostPayload) -> OrderPostPayload:
        pass

class HardCodedOrders(OrderRepository):

    orders: dict[str, OrderDatabaseEntry] = {}
    
    def post_order(self, order: OrderDatabaseEntry) -> OrderDatabaseEntry:
        self.orders[order.order_id] = order
    
    def get_order_by_id(self, id: str) -> Optional[OrderDatabaseEntry]:
        return self.orders[id] if id in self.orders else None