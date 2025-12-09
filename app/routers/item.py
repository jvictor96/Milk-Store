from fastapi.security import  OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Query, Path, HTTPException, Depends
from typing import Annotated
from fastapi import APIRouter
from domain.model.item import Item
from persistence.item_repository import ItemRepository
from typing import Literal
from pydantic import BaseModel, Field

class FilterParams(BaseModel):
    model_config = {"extra": "forbid"}
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []

item_repository : ItemRepository

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/items/")
async def read_items(filter_query: Annotated[FilterParams, Query()], token: Annotated[str, Depends(oauth2_scheme)]):
    return {"item_id": "item_id", "q": "q"}

@router.get("/items/{item_id}")
def read_item(item_id: Annotated[int, Path(gt=1000)], q: Annotated[str | None, Query(max_length=5)] = None):
    if item_id not in item_repository.get_all_items():
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id": item_id, "q": q}

@router.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}

@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return {"access_token": form_data.username, "token_type": "bearer"}