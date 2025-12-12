from abc import ABC, abstractmethod
from domain.schemas.order import Order

class OrderRepositoryPort(ABC):
    @abstractmethod
    def post_order(self, batch: Order) -> Order:
        pass
    @abstractmethod
    def get_order_by_id(self, batch: Order) -> Order:
        pass