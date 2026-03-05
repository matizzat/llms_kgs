from llms_kgs.persistence import CMapRetriever, CMapDeleter
from llms_kgs.core_utils import log_error, Notification

class CMapRemover:
    """
    Orchestrates the logic for removing a concept map
    from the knowledge base. 
    """

    def __init__(self, retriever: CMapRetriever, deleter: CMapDeleter):

        self._retriever = retriever
        self._deleter = deleter 

    def remove_by_title(self, title: str) -> Notification:
        
        notification = Notification()

        try:

            if not self._retriever.exists_by_title(title):
       
                notification.add_error(f"Concept map with title '{title}' doesn't exist.")
                return notification

            self._deleter.delete_by_title(title)

        except Exception as e:
            log_error('CMapRemover', 'remove_by_title', e)
            notification.add_error("An unexpected error occurred. See log for more details.")

        return notification

