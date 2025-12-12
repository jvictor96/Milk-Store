class Order():
    qty: float
    order_id: str
    batch_code: str

    def __init__(self, qty: float, order_id: str, batch_id: str):
        self.qty = qty
        self.order_id = order_id
        self.batch_code = batch_id
