import datetime
from typing import Annotated

from fastapi import HTTPException
from api.schemas.near_expiry_filter_params import NearExpiryFilterParams
from domain.schemas.batch_database_entry import BatchDatabaseEntry
from domain.schemas.batch_post_payload import BatchPostPayload
from domain.schemas.batch_get_response import BatchGetResponse
from domain.schemas.order_post_payload import OrderPostPayload
from repositories.batch_repository import BatchRepository


batch_repository : BatchRepository

def post_batch(batch: BatchPostPayload) -> BatchGetResponse:
    entry = BatchDatabaseEntry(batch)
    batch_repository.post_batch(entry)
    return entry

def get_active_batches() -> list[BatchGetResponse]:
    batch_repository.get_active_batches_until_date(datetime.datetime.now())

def get_batch_by_id(id: str) -> BatchGetResponse:
    batch_repository.get_batch_by_id(id)

def consume(batch_id: str, consume_post_payload: OrderPostPayload) -> OrderPostPayload:
    entry = batch_repository.get_batch_by_id(batch_id)
    if not entry :
        raise HTTPException(status_code=404, detail="Item not found")
    if entry.consumed + consume_post_payload.qty > entry.volume_liters:
        raise HTTPException(status_code=409, detail="Consumed volume exceeds liters available")
    pass

async def get_near_expiry(filter_params: NearExpiryFilterParams):
    check_until_day = datetime.datetime.now() + datetime.timedelta(days = filter_params.n_days)
    batch_repository.get_active_batches_until_date(check_until_day)

def delete_batch_by_id(id: str):
    batch_repository.delete_batch(id)