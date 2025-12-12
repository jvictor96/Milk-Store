from api.schemas.order_dto import OrderDto
from domain.schemas.order import Order


class OrderMapper():
    @staticmethod
    def to_domain(order: OrderDto, batch_code:str) -> Order:
        return Order(
            order.qty,
            order.order_id,
            batch_code
        )
    
    @staticmethod
    def to_dto(order: Order) -> OrderDto:
        return OrderDto(
            qty = order.qty,
            order_id = order.order_id,
            batch_code = order.batch_code
        )