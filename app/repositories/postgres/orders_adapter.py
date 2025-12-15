from typing import Optional

from sqlmodel import Session, select
from repositories.mappers.order_mapper import OrderMapper
from repositories.schemas.order_entity import OrderEntity
from domain.ports.order_repository_port import OrderRepositoryPort
from domain.schemas.order import Order
from .postgres_connection import engine

class OrdersAdapter(OrderRepositoryPort):
    
    def post_order(self, batch: Order) -> Order:
        batch_entity = OrderMapper.to_entity(batch)
        with Session(engine) as session:
            session.add(batch_entity)
            session.commit()
            session.refresh(batch_entity)
        return OrderMapper.to_domain(batch_entity)
    
    def get_order_by_id(self, id: str) -> Optional[Order]:
        with Session(engine) as session:
            stmt = select(OrderEntity).where(OrderEntity.order_id == id)
            result = session.exec(stmt)
        return result.first