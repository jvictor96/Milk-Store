from fastapi import Query, Path, HTTPException, Depends
from typing import Annotated
from fastapi import APIRouter
from domain.schemas.batch_post_payload import BatchPostPayload
from domain.schemas.order_post_payload import OrderPostPayload
from domain.service import batch_service
from .schemas.near_expiry_filter_params import NearExpiryFilterParams
from repositories.batch_repository import HardCodedBatches

router = APIRouter()
batch_service.batch_repository = HardCodedBatches()

@router.post("/api/batches/")
async def post_batch(batch: BatchPostPayload):
    return batch_service.post_batch(batch)

@router.get("/api/batches/")
async def get_active_batches(batch: BatchPostPayload):
    return batch_service.get_active_batches(batch)

# TODO: validate date format
@router.get("/api/batches/{id}")
async def get_batch_by_id(id: Annotated[str, Path(pattern='^SCH-\\d{8}-\\d{4}$')]):
    return batch_service.get_batch_by_id(id)

@router.post("/api/batches/{id}/consume")
async def consume(id: str, consume_post_payload: OrderPostPayload):
    return batch_service.consume(id, consume_post_payload)

@router.get("/api/batches/near-expiry/")
async def get_near_expiry(filter_query: Annotated[NearExpiryFilterParams, Query()]):
    return {"item_id": "item_id", "q": "q"}

def delete_batch_by_id(id: str):
    batch_service.delete_batch_by_id(id)