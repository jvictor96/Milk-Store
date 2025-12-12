class NotUniqueException(Exception):
    def __init__(self, property: str):
        super().__init__(f"{property} is not unique")