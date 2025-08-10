import uuid

class IDGenerator:
    
    @staticmethod
    def generate_id():
        """Generates a unique ID."""
        return str(uuid.uuid4())

    @staticmethod
    def is_valid_id(uid):
        """Checks if the provided budget ID is valid."""
        try:
            # Validate if the ID is a valid UUID format
            uuid_obj = uuid.UUID(uid, version=4)
            return str(uuid_obj) == uid
        except ValueError:
            return False
