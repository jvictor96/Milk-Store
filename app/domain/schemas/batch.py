import datetime

class Batch():
    batch_code: str
    received_at: datetime.datetime
    expiry_date: datetime.datetime 
    deleted_at: datetime.datetime
    volume_liters: float
    fat_percent: float
    consumed: float

    @staticmethod
    def calculate_expiry_date(received_at: datetime.datetime, shelf_life_days: datetime.timedelta) -> datetime.datetime:
        return received_at + shelf_life_days
    
    def get_shelf_life_days_as_int(self) -> int:
        return (self.expiry_date - self.received_at).days
    

    def __init__(self,
                 batch_code: str,
                 received_at: datetime.datetime,
                 volume_liters: float,
                 fat_percent: float,
                 shelf_life_days: datetime.timedelta,):
        self.batch_code = batch_code
        self.received_at = received_at
        self.volume_liters = volume_liters
        self.fat_percent = fat_percent
        self.expiry_date = Batch.calculate_expiry_date(received_at, shelf_life_days)
        self.consumed = 0
        self.deleted_at = None

        