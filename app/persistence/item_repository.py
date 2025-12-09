from abc import ABC, abstractmethod

class ItemRepository(ABC):
    @abstractmethod
    def get_all_items():
        pass

class HardCodedItems(ItemRepository):
    def get_all_items():
        return {"foo": "The Foo Wrestlers"}