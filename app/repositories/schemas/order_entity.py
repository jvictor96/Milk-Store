import datetime
from sqlmodel import Field, SQLModel

from dependencies import settings


class OrderEntity(SQLModel, table=True):
    order_id: str = Field(regex='^ORDER-\\d{8}-\\d{4}$', primary_key = True)
    batch_code: str = Field(regex='^SCH-\\d{8}-\\d{4}$')
    qty: float = Field(7, gt=0)

    def get_order_id_as_datetime(self) -> datetime.datetime:
        return datetime.datetime.strptime(self.order_id[6:14], settings.datetime_string_formats.order_id)

    def get_batch_code_as_datetime(self) -> datetime.datetime:
        return datetime.datetime.strptime(self.batch_code[4:12], settings.datetime_string_formats.batch_code)