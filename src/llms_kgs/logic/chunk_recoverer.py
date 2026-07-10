from llms_kgs.core_utils import log_error, Notification
from llms_kgs.persistence import ChunkRepository
from typing import List, Dict
from llms_kgs.domain import Chunk

class ChunkRecoverer:

    def __init__(self, repository: ChunkRepository):

        self._repository = repository

    def recover_titles(self) -> Dict[Notification, List[str]]:

        notification = Notification()
        titles = []

        try:

            titles = self._repository.retrieve_titles() 
       
        except Exception as e:

            log_error('ChunkRecoverer', 'recover_titles', e)
            notif.add_error('An unexpected error ocurred! See log for details.')

        return {'notification': notification, 'titles': titles}        

    def recover_all(self) -> Dict[Notification, List[Chunk]]:

        notification = Notification()
        chunks = []

        try:

            chunks = self._repository.retrieve_all()

        except Exception as e:

            log_error('ChunkRecoverer', 'recover_all', e)
            notif.add_error('An unexpected error ocurred! See log for details.')

        return {'notification': notification, 'chunks': chunks}

    def recover_by_title(self, title: str) -> Dict[Notification, Chunk | None]:

        notification = Notification()
        chunk = None 

        try:
            
            chunk = self._repository.retrieve_by_title(title)
        
            if chunk == None:
                notification.add_error(f"Chunk with title '{title}' doesn't exist")
            
        except Exception as e:

            log_error('ChunkRecoverer', 'recoveer_by_title', e)
            notification.add_error('An unexpected error ocurred! See log for details.')

        return {'notification': notification, 'chunk': chunk}
