from fastapi import FastAPI
from api import batches_api

app = FastAPI()
app.include_router(batches_api.router)
