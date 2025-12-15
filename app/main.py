from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from api import batches_api
from domain.service.batch_service import BatchService
from domain.ports.batch_repository_port import BatchRepositoryPort
from domain.ports.order_repository_port import OrderRepositoryPort
from domain.exceptions.conflict_exception import ConflictException
from domain.exceptions.not_found_exception import NotFoundException
from domain.exceptions.not_unique_exception import NotUniqueException
from dependencies import env_container

# TODO: Write tests
# TODO: Write the README
app = FastAPI()
batch_router = batches_api.get_router(BatchService(env_container[BatchRepositoryPort], env_container[OrderRepositoryPort]))
app.include_router(batch_router)

@app.exception_handler((RequestValidationError)) # TODO: move the error handler
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )

@app.exception_handler(NotFoundException)
async def not_found_handler(request: Request, exc: NotFoundException):
    return JSONResponse(
        status_code=404,
        content=jsonable_encoder({"detail": exc.args}),
    )

@app.exception_handler(NotUniqueException)
async def not_found_handler(request: Request, exc: NotUniqueException):
    return JSONResponse(
        status_code=409,
        content=jsonable_encoder({"detail": exc.args}),
    )

@app.exception_handler(ConflictException)
async def not_found_handler(request: Request, exc: ConflictException):
    return JSONResponse(
        status_code=409,
        content=jsonable_encoder({"detail": exc.args}),
    )
