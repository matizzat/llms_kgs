from llms_kgs.persistence import CMapRetriever, CMapInserter
from llms_kgs.core_utils import log_error, Notification
from llms_kgs.llms import EncoderProtocol
from llms_kgs.domain import CMap
from .cmap_encoder import CMapEncoderProtocol

class CMapAdder:
    """
    Orchestrates the logic for adding a concept map
    into the knowledge base. 
    """

    def __init__(
            self,
            retriever: CMapRetriever,
            cmap_encoder: CMapEncoderProtocol,
            ef: EncoderProtocol,
            inserter: CMapInserter):
      
        self._cmap_encoder = cmap_encoder
        self._retriever = retriever
        self._inserter = inserter
        self._ef = ef

    def add(self, cmap: CMap) -> Notification:

        notification = Notification()
       
        try:

            if not cmap.is_valid(notification):
                return notification 

            if self._retriever.exists_by_title(cmap.title):
           
                notification.add_error(f"Concept map with title '{cmap.title}' already exists.")
                return notification 
       
            cmap.embedding = self._cmap_encoder.encode(cmap)

            for triple in cmap.triples:
                triple.embedding = self._ef.encode(triple.to_sentence())
            
            self._inserter.insert(cmap)

        except Exception as e:

            log_error("CMapAdder", "add", e) 
            notification.add_error("An unexpected error ocurred. See log for more details.")

        return notification
