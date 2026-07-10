class Notification:

    def __init__(self):
        self._errors = []

    def add_error(self, message: str):
        self._errors.append(message)
 
    def has_errors(self) -> bool:
        return len(self._errors) > 0

    def get_errors(self) -> list:
        return self._errors

    def to_dict(self) -> dict:
        """Serializes the notification state."""
   
        return {"errors": self._errors}

    @classmethod
    def from_dict(cls, data: dict) -> 'Notification':
        """Reconstructs a Notification object from a dictionary."""
    
        notification = cls()
        notification._errors = data.get("errors", [])
        return notification
  
