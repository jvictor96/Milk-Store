from repositories.schemas.order_entity import OrderEntity
from domain.schemas.order import Order


class OrderMapper():
    @staticmethod
    def to_domain(order: OrderEntity, batch_code:str) -> Order:
        order.batch_code = batch_code
        return Order(
            order.qty,
            order.order_id,
            order.get_order_id_as_datetime(),
            batch_code,
            order.get_batch_code_as_datetime(),
        )
    
    @staticmethod
    def to_dto(order: Order) -> OrderEntity:
        return OrderEntity(
            qty = order.qty,
            order_id = order.order_id,
            batch_code = order.batch_code
        )