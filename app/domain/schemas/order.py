import datetime


class Order():
    qty: float
    order_id: str
    order_id_date: datetime.datetime
    batch_code: str
    batch_code_date: datetime.datetime

    def __init__(self, qty: float, order_id: str, order_id_date: datetime, batch_id: str, batch_code_date: datetime.datetime):
        self.qty = qty
        self.order_id = order_id
        self.batch_code = batch_id
        self.order_id_date = order_id_date
        self.batch_code_date = batch_code_date
