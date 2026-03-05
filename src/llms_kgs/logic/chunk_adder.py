from llms_kgs.core_utils import log_error, Notification 
from llms_kgs.persistence import ChunkRepository
from .chunk_encoder import ChunkEncoder
from llms_kgs.domain import Chunk

class ChunkAdder: 

    def __init__(self, repository: ChunkRepository, chunk_encoder: ChunkEncoder):

        self._repository = repository 
        self._chunk_encoder = chunk_encoder 

    def add(self, title: str, text: str) -> Notification:
        
        notification = Notification()
        try:

            chunk = Chunk(title=title, text=text)
            
            if not chunk.is_valid(notification):
                return notification 

            if self._repository.exists_by_title(chunk.title):
                notification.add_error(f"Chunk with title '{chunk.title}' already exists.")
                return notification 

            chunk.embedding = self._chunk_encoder.encode(chunk)
            self._repository.insert(chunk)

        except Exception as e:
            log_error('ChunkAdder', 'add', e)
            notification.add_error("An unexpected error occurred. See log for more details.")

        return notification
