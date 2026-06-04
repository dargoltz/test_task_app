import uuid


class EntityNotFoundError(Exception):
    def __init__(self, entity: type, entity_id: uuid.UUID):
        super().__init__(f"{entity.__name__} {entity_id} not found")
