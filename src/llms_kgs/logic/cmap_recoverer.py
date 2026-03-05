from llms_kgs.core_utils import log_error, Notification
from llms_kgs.persistence import CMapRetriever 
from typing import List, Dict, Tuple
from llms_kgs.domain import CMap

class CMapRecoverer:
    """
    Orchestrates the logic for recovering concept maps
    from the knowledge base according to different criteria.
    """

    def __init__(self, retriever: CMapRetriever):

        self._retriever = retriever 

    def recover_titles(self) -> Tuple[Notification, List[str]]: 

        notification = Notification()
        titles = []

        try:

            titles = self._retriever.retrieve_titles()

        except Exception as e:

            log_error('CMapRecoverer', 'recover_titles', e) 
            notification.add_error("An unexpected error ocurred. See log for more details.")

        return notification, titles

    def recover_by_title(self, title: str) -> Dict[Notification, CMap | None]:

        notification = Notification()
        cmap = None 

        try:

            cmap = self._retriever.retrieve_by_title(title)

            if(cmap == None):
                notification.add_error(f"CMap with title '{title}' doesn't exist.")
    
        except Exception as e:

            log_error('CMapRecoverer', 'recover_by_title', e) 
            notification.add_error("An unexpected error ocurred. See log for more details.")

        return {'notification': notification, 'cmap': cmap}
