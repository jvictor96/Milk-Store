class NotFoundException(Exception):
    def __init__(self, entity_name: str):
        super().__init__(f"{entity_name} is not found")