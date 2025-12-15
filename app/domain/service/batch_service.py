import datetime

from domain.exceptions.not_found_exception import NotFoundException
from domain.exceptions.not_unique_exception import NotUniqueException
from domain.exceptions.conflict_exception import ConflictException
from domain.ports.batch_repository_port import BatchRepositoryPort
from domain.ports.order_repository_port import OrderRepositoryPort
from domain.schemas.batch import Batch
from domain.schemas.order import Order


batch_repository : BatchRepositoryPort
order_repository : OrderRepositoryPort

def post_batch(batch: Batch) -> Batch:
    if batch_repository.get_batch_by_id(batch.batch_code):
        raise NotUniqueException("batch_code")
    batch_repository.post_batch(batch)
    return batch

def get_active_batches() -> list[Batch]:
    return batch_repository.get_active_batches()

def get_batch_by_id(id: str) -> Batch:
    batch = batch_repository.get_batch_by_id(id)
    if not batch:
        raise NotFoundException("batch")
    return batch

def consume(batch_id: str, order: Order) -> Order:
    if order_repository.get_order_by_id(order.order_id):    #TODO: implement locks
        raise NotUniqueException("order_id")
    batch = batch_repository.get_batch_by_id(batch_id)
    if batch == None or batch.deleted_at:
        raise NotFoundException("Batch")
    if batch.consumed + order.qty > batch.volume_liters:
        raise ConflictException("Consumed volume exceeds liters available")
    if order.order_id_date < order.batch_code_date:
        raise ConflictException("order is registered before batch")
    batch.consumed = batch.consumed + order.qty
    batch_repository.update_batch(batch)
    order_repository.post_order(order)
    order.batch_code = batch_id
    return order


def get_near_expiry(n_days: int) -> list[Batch]:
    check_until_day = datetime.datetime.now() + datetime.timedelta(days = n_days)
    return batch_repository.get_active_batches_until_date(check_until_day)

def delete_batch_by_id(id: str):
    batch = batch_repository.get_batch_by_id(id)
    if not batch:
        raise NotFoundException("batch")
    batch.deleted_at = datetime.datetime.now()
    batch_repository.update_batch(batch)