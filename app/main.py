from fastapi import FastAPI
from persistence.item_repository import HardCodedItems
from routers import item

item.item_repository = HardCodedItems()

app = FastAPI()
app.include_router(item.router)
