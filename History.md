# c6c2027 boiler plate

Was just almost the simplest implementation of an api that does nothing and was based on the documentation examples found here https://fastapi.tiangolo.com/tutorial/. 

## Structure

```
├── requirements.py
├── .gitignore
└── app
    ├── main.py
    ├── dependencies.py (empty)
    ├── domain/model
    │   └── image.py
    │   └── item.py
    ├── persistence
    │   └── item_repository.py
    └── routers
        ├── exception_handler.py
        └── item.py
```

## Architecture and theory

At this stage, I've introduced polymorphysm to create an interface between domain and persistence at item_repository.py. It's much based on Clean Architecture and taking care of layer isolation and the graph of dependencies.


``` python
from abc import ABC, abstractmethod

class ItemRepository(ABC):          # That port was renamed to BatchRepositoryPort moved to the domain package later
    @abstractmethod
    def get_all_items():
        pass

class HardCodedItems(ItemRepository):
    def get_all_items():
        return {"foo": "The Foo Wrestlers"}
```

At routers/item.py there was a fragment to use ItemRepository reguardless the implementation
At main.py there was a fragment to inject HardCodedItems


## ade898a business rules

This was the fist attempt to implement the specification. Manual tests were run and the API worked as expected at the following commit. TDD was not considered at this point and the models were not well separated.

## Structure

```
├── requirements.py
├── .gitignore
└── app
    ├── main.py
    ├── dependencies.py (empty)
    ├── domain
    │   ├── schemas ( *1 )
    │   │    ├── batch_database_entry.py
    │   │    ├── batch_post_payload.py
    │   │    ├── order_database_entry.py
    │   │    ├── order_post_payload.py
    │   │    └── batch_get_response.py
    │   └── services
    │        └── batch_service.py
    ├── repositories (renamed)
    │   ├── batch_repository.py
    │   └── order_repository.py
    └── api
        ├── exception_handler.py
        ├── batches_api.py
        └── schemas
             └── near_expiry_filter_params.py
```

1: many api schemas were here because I wanted to keep the domain packge without any import from api and I lacked mappers yet, so I worked with the post payload models at the service. The domain was isolated, but poorly organized.


I've probably started with batches_api.py writing the endpoints to fulfill the spec


``` python
router = APIRouter()
batch_service.batch_repository = HardCodedBatches()

@router.post("/api/batches/")
async def post_batch(batch: BatchPostPayload):
    return batch_service.post_batch(batch)

@router.get("/api/batches/")
async def get_active_batches(batch: BatchPostPayload):
    return batch_service.get_active_batches(batch)

@router.get("/api/batches/{id}")
async def get_batch_by_id(id: Annotated[str, Path(pattern='^SCH-\\d{8}-\\d{4}$')]):
    return batch_service.get_batch_by_id(id)

@router.post("/api/batches/{id}/consume")
async def consume(id: str, consume_post_payload: OrderPostPayload):
    return batch_service.consume(id, consume_post_payload)

@router.get("/api/batches/near-expiry/")
async def get_near_expiry(filter_query: Annotated[NearExpiryFilterParams, Query()]):
    return {"item_id": "item_id", "q": "q"}  # Oh forgive me

def delete_batch_by_id(id: str):
    batch_service.delete_batch_by_id(id)
```

If I were using TDD, CI, extreme programming and agile I'd have written tests for post_batch, get_active_batches, get_batch_by_id, consume, get_near_expiry and delete_batch_by_id immediatelly.

Repository structure was prety much the same, with the port declared at the repository layer, which is bad for my domain isolation as Clear architecture states.

# 6941e72 test validation

Same structure but works. Domain logic wasn't touched deeply since, maybe this domain is to simple and I can't use advanced DDD to make good diagrams, but being isolated might help in having a clear code to express the business logic.


# 8785ea6 isolate domain using repository adapters and read properties from yaml

Several improvements but mainly moving API's schemas to the API package, writing mappers, putting persistence ports at the domain layer, writing my domain exceptions and putting hardcoded values at properties.yaml. Clean Architecture is here now.

## Structure

```
├── requirements.py
├── .gitignore
└── app
    ├── main.py
    ├── dependencies.py (it's meant to be a di_container but I've used to keep my property helper)
    ├── properties.yaml (new file)
    ├── domain
    │   ├── exceptions (new package)
    │   │    ├── ConflictException.py (ops, camel case)
    │   │    ├── NotFoundException.py
    │   │    └── NotUniqueException.py
    │   ├── ports (new package)
    │   │    ├── batch_repository_port.py
    │   │    └── order_repository_port.py
    │   ├── schemas (this package is free of any 'SCH-12345678-1324' sort of formatting clue now, as it's part of the api spec)
    │   │    ├── order.py
    │   │    └── batch.py
    │   └── services
    │        └── batch_service.py
    ├── repositories (these are still just in-memory implementations)
    │   ├── batch_repository.py
    │   └── order_repository.py
    └── api
        ├── exception_handler.py
        ├── batches_api.py
        ├── mappers
        │    ├── batch_mapper.py
        │    └── order_mapper.py
        └── schemas
             ├── batch_dto.py
             ├── near_expiry_filter_params.py
             └── order_dto.py
```

## 7eb06ac add examples, several minor formatting improvements, handle errors

OpenAPI is much better now

## da59d9a create sqlmodel models and repository and use properties examples all across

repositories/mappers and repositories/schemas were added to write model code that bootstraps sqlmodel and keep the domain package free of it. Also repositories/postgres was added. Clean Architecture for ever

## 524e2a0 add tests

tests finally added. All knowledge about TDD, CI, extreme programming, agile and refactoring were not known before, so I had huge commits and no tests so far.