from llms_kgs.core_utils import Notification

class Query:
    _min_len = 1

    def __init__(self, query: str): 
        self.text = self.normalize(query)

    def normalize(self, query: str) -> str:
        
        normalized = query.strip()
        return normalized

    def is_valid(self, notif: Notification) -> bool: 

        if(len(self.text) < self._min_len):
            notif.add_error(f'Query must have at least {self._min_len} character/s.')
            return False

        return True 

    def get(self) -> str:
        return self.text
