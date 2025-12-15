import datetime

from domain.exceptions.not_found_exception import NotFoundException
from domain.exceptions.not_unique_exception import NotUniqueException
from domain.exceptions.conflict_exception import ConflictException
from domain.ports.batch_repository_port import BatchRepositoryPort
from domain.ports.order_repository_port import OrderRepositoryPort
from domain.schemas.batch import Batch
from domain.schemas.order import Order


class BatchService():
    batch_repository : BatchRepositoryPort
    order_repository : OrderRepositoryPort

    def __init__(self, batch_repository: BatchRepositoryPort, order_repository: OrderRepositoryPort):
        self.batch_repository = batch_repository
        self.order_repository = order_repository

    def post_batch(self, batch: Batch) -> Batch:
        if self.batch_repository.get_batch_by_id(batch.batch_code):
            raise NotUniqueException("batch_code")
        self.batch_repository.post_batch(batch)
        return batch

    def get_active_batches(self) -> list[Batch]:
        return self.batch_repository.get_active_batches()

    def get_batch_by_id(self, id: str) -> Batch:
        batch = self.batch_repository.get_batch_by_id(id)
        if not batch:
            raise NotFoundException("batch")
        return batch

    def consume(self, batch_id: str, order: Order) -> Order:
        if self.order_repository.get_order_by_id(order.order_id):    #TODO: implement locks
            raise NotUniqueException("order_id")
        batch = self.batch_repository.get_batch_by_id(batch_id)
        if batch == None or batch.deleted_at:
            raise NotFoundException("Batch")
        if batch.consumed + order.qty > batch.volume_liters:
            raise ConflictException("Consumed volume exceeds liters available")
        if order.order_id_date < order.batch_code_date:
            raise ConflictException("order is registered before batch")
        batch.consumed = batch.consumed + order.qty
        self.batch_repository.update_batch(batch_id, batch)
        self.order_repository.post_order(order)
        order.batch_code = batch_id
        return order


    def get_near_expiry(self, n_days: int) -> list[Batch]:
        check_until_day = datetime.datetime.now() + datetime.timedelta(days = n_days)
        return self.batch_repository.get_active_batches_until_date(check_until_day)

    def delete_batch_by_id(self, id: str):
        batch = self.batch_repository.get_batch_by_id(id)
        if not batch:
            raise NotFoundException("batch")
        batch.deleted_at = datetime.datetime.now()
        self.batch_repository.update_batch(id, batch)