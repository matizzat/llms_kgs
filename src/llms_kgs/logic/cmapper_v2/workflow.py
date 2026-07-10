from .cmap_creation_state import CMapCreationState

from .focus_question_extractor import FocusQuestionExtractor
from .concepts_extractor import ConceptsExtractor
from .relations_extractor import RelationsExtractor
from .triples_extractor import TriplesExtractor 
from .improvement_extractor import ImprovementExtractor 

from llms_kgs.domain import Chunk

class CMapCreationWorkflow:
    """
    Orchestrator of the concept map creation workflow.
    """

    def __init__(self,
            focus_question_extractor: FocusQuestionExtractor,
            concepts_extractor: ConceptsExtractor,
            relations_extractor: RelationsExtractor,
            triples_extractor: TriplesExtractor,
            improvement_extractor: TriplesExtractor): 
                       
        self._focus_question_extractor = focus_question_extractor
        self._concepts_extractor = concepts_extractor
        self._relations_extractor = relations_extractor
        self._triples_extractor = triples_extractor
        self._improvement_extractor = improvement_extractor
    
    def create_cmap(self, chunk: Chunk, max_improvements: int = 0) -> CMapCreationState:
        state = CMapCreationState(chunk)
        
        self._focus_question_extractor.extract(state)
        self._concepts_extractor.extract(state)
        self._relations_extractor.extract(state)
        self._triples_extractor.extract(state)

        for _ in range(max_improvements):
            self._improvement_extractor.extract(state)

            if state.has_converged():
                break

        return state
