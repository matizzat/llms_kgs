from llms_kgs.core_utils import log_error, Notification
from llms_kgs.persistence import ChunkRepository

class ChunkRemover:

    def __init__(self, repository: ChunkRepository):

        self._repository = repository

    def remove_by_title(self, title: str) -> Notification:

        notification = Notification()
        try:

            if not self._repository.exists_by_title(title):

                notification.add_error(f"Chunk with title '{title}' doesn't exist.")
                return notificiation

            self._repository.delete_by_title(title)

        except Exception as e:

            log_error('ChunkRemover', 'remove_by_title', e)
            notification.add_error("An unexpected error occurred. See log for more details.")

        return notification
