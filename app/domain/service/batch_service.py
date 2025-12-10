import datetime

from fastapi import HTTPException
from api.schemas.near_expiry_filter_params import NearExpiryFilterParams
from domain.schemas.order_database_entry import OrderDatabaseEntry
from repositories.order_repository import OrderRepository                 # TODO: move the repository innterfaces to the domain package
from domain.schemas.batch_database_entry import BatchDatabaseEntry
from domain.schemas.batch_post_payload import BatchPostPayload
from domain.schemas.batch_get_response import BatchGetResponse
from domain.schemas.order_post_payload import OrderPostPayload
from repositories.batch_repository import BatchRepository


batch_repository : BatchRepository
order_repository : OrderRepository

def post_batch(batch: BatchPostPayload) -> BatchGetResponse:
    if batch_repository.get_batch_by_id(batch.batch_code):
        raise HTTPException(status_code=409, detail="Not unique batch_code")
    entry = BatchDatabaseEntry.build(batch)
    batch_repository.post_batch(entry)
    return entry

def get_active_batches() -> list[BatchGetResponse]:
    return batch_repository.get_active_batches()

def get_batch_by_id(id: str) -> BatchGetResponse:
    return batch_repository.get_batch_by_id(id)

def consume(batch_id: str, consume_post_payload: OrderPostPayload) -> OrderPostPayload:
    if order_repository.get_order_by_id(consume_post_payload.order_id):
        raise HTTPException(status_code=409, detail="Not unique order_id")
    entry = batch_repository.get_batch_by_id(batch_id)
    if entry == None:
        raise HTTPException(status_code=404, detail="Item not found")
    if entry.consumed + consume_post_payload.qty > entry.volume_liters:
        raise HTTPException(status_code=409, detail="Consumed volume exceeds liters available")
    entry.consumed = entry.consumed + consume_post_payload.qty
    batch_repository.update_batch(entry)
    order = OrderDatabaseEntry.build(consume_post_payload, batch_id)
    order_repository.post_order(order)


def get_near_expiry(filter_params: NearExpiryFilterParams) -> list[BatchDatabaseEntry]:
    check_until_day = datetime.datetime.now() + datetime.timedelta(days = filter_params.n_days)
    return batch_repository.get_active_batches_until_date(check_until_day)

def delete_batch_by_id(id: str):
    batch_repository.delete_batch(id)