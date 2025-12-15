from typing import Optional
from domain.ports.order_repository_port import OrderRepositoryPort
from domain.schemas.order import Order

class InMemoryOrders(OrderRepositoryPort):

    orders: dict[str, Order] = {}
    
    def post_order(self, order: Order) -> Order:
        self.orders[order.order_id] = order
    
    def get_order_by_id(self, id: str) -> Optional[Order]:
        return self.orders[id] if id in self.orders else None