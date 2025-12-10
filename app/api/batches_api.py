from fastapi import Body, Query, Path
from typing import Annotated
from fastapi import APIRouter
from repositories.order_repository import HardCodedOrders
from domain.schemas.batch_post_payload import BatchPostPayload, check_batch_timestamps
from domain.schemas.order_post_payload import OrderPostPayload, check_order_timestamps
from domain.service import batch_service
from .schemas.near_expiry_filter_params import NearExpiryFilterParams
from repositories.batch_repository import HardCodedBatches
from pydantic import AfterValidator

router = APIRouter()
batch_service.batch_repository = HardCodedBatches()
batch_service.order_repository = HardCodedOrders()

@router.post("/api/batches/")
async def post_batch(batch: Annotated[BatchPostPayload, Body(embed=True), AfterValidator(check_batch_timestamps)]):
    return batch_service.post_batch(batch)

@router.get("/api/batches/")
async def get_active_batches():
    return batch_service.get_active_batches()

# TODO: validate date format
@router.get("/api/batches/{id}")
async def get_batch_by_id(id: Annotated[str, Path(pattern='^SCH-\\d{8}-\\d{4}$')]):
    return batch_service.get_batch_by_id(id)

@router.post("/api/batches/{id}/consume")
async def consume(id: str, consume_post_payload: Annotated[OrderPostPayload, Body(embed=True), AfterValidator(check_order_timestamps)]):
    return batch_service.consume(id, consume_post_payload)

@router.get("/api/batches/near-expiry/")
async def get_near_expiry(filter_query: Annotated[NearExpiryFilterParams, Query()]):
    return batch_service.get_near_expiry(filter_query)

@router.delete("/api/batches/{id}")
def delete_batch_by_id(id: str):
    batch_service.delete_batch_by_id(id)