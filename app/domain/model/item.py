from typing import Union, List
from pydantic import BaseModel
from .image import Image

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: List[str] = []
    image: Image | None = None