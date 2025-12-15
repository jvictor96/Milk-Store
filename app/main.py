from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from api import batches_api
from domain.exceptions.conflict_exception import ConflictException
from domain.exceptions.not_found_exception import NotFoundException
from domain.exceptions.not_unique_exception import NotUniqueException
import repositories.postgres.postgres_connection

# TODO: Write tests
# TODO: Write the README
app = FastAPI()

app.include_router(batches_api.router)

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
