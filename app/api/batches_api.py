from fastapi import Body, Query, Path
from typing import Annotated
from fastapi import APIRouter
from api.mappers.batch_mapper import BatchMapper
from api.mappers.order_mapper import OrderMapper
from repositories.in_memory_batches import InMemoryBatches
from repositories.in_memory_orders import InMemoryOrders
from api.schemas.batch_dto import BatchDTO
from api.schemas.order_dto import OrderDto
from domain.service import batch_service
from .schemas.near_expiry_filter_params import NearExpiryFilterParams
from dependencies import settings

router = APIRouter()
batch_service.batch_repository = InMemoryBatches()
batch_service.order_repository = InMemoryOrders()

@router.post("/api/batches/")
async def post_batch(batch_dto: Annotated[BatchDTO, Body()]):
    return BatchMapper.to_dto(batch_service.post_batch(BatchMapper.to_domain(batch_dto)))

@router.get("/api/batches/")
async def get_active_batches():
    return [BatchMapper.to_dto(batch) for batch in batch_service.get_active_batches()]

@router.get("/api/batches/{id}")
async def get_batch_by_id(id: Annotated[str, Path(pattern=settings.string_patterns.batch_code, example=settings.examples.batch_code)]):
    return BatchMapper.to_dto(batch_service.get_batch_by_id(id))

@router.post("/api/batches/{id}/consume")
async def consume(id: Annotated[str, Path(pattern=settings.string_patterns.batch_code, example=settings.examples.batch_code)], 
                  order_dto: Annotated[OrderDto, Body()]):
    return OrderMapper.to_dto(batch_service.consume(id, OrderMapper.to_domain(order_dto, id)))

@router.get("/api/batches/near-expiry/")
async def get_near_expiry(filter_query: Annotated[NearExpiryFilterParams, Query()]):
    return [BatchMapper.to_dto(batch) for batch in batch_service.get_near_expiry(filter_query.n_days)]

@router.delete("/api/batches/{id}")
def delete_batch_by_id(id: Annotated[str, Path(pattern=settings.string_patterns.batch_code, example=settings.examples.batch_code)]):
    batch_service.delete_batch_by_id(id)