import datetime

from domain.exceptions import ConflictException, NotFoundException, NotUniqueException
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

def consume(batch_id: str, order: Order) -> Order:    # TODO: validate if the order date is after the batch date
    if order_repository.get_order_by_id(order.order_id):
        raise NotUniqueException("order_id")
    entry = batch_repository.get_batch_by_id(batch_id)
    if entry == None:
        raise NotFoundException("Batch")
    if entry.consumed + order.qty > entry.volume_liters:
        raise ConflictException("Consumed volume exceeds liters available")
    entry.consumed = entry.consumed + order.qty
    batch_repository.update_batch(entry)
    order_repository.post_order(order)
    order.batch_code = batch_id
    return order


def get_near_expiry(n_days: int) -> list[Batch]:
    check_until_day = datetime.datetime.now() + datetime.timedelta(days = n_days)
    return batch_repository.get_active_batches_until_date(check_until_day)

def delete_batch_by_id(id: str):
    batch_repository.delete_batch(id)