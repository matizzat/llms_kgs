# cmapper_v2/cmap_creation_state.py

from llms_kgs.domain import Triple, Chunk
from llms_kgs.llms import LLMInvocationData

from dataclasses import dataclass, field
from typing import Optional, List

@dataclass
class CMapCreationState:
    """
    Common workspace of the concept map creation process. Holds the
    input chunk and the intermediate results produced by each
    information extractor. Provides helper functions to store data
    and check the state of the current concept map - i.e. whether 
    the triples improvement algorithm converged. 
    """

    # Input: 
    chunk: Chunk

    # Outputs:
    focus_question: Optional[str] = None
    concepts: Optional[List[str]] = None
    relations: Optional[List[str]] = None
    triples_refinements: Optional[List[List[Triple]]] = None

    # Runtime log:  
    invocations: List[LLMInvocationData] = field(default_factory = list) 

    # Methods:
    def add_invocation(self, invocation: LLMInvocationData):

        self.invocations.append(invocation)
    

    def add_refinement(self, triples: List[Triple]):

        if not self.triples_refinements:
            self.triples_refinements = [triples]

        else:
            self.triples_refinements.append(triples)

    def has_converged(self) -> bool:

        if not self.triples_refinements or len(self.triples_refinements) < 2:
            return False

        for triple in self.triples_refinements[-1]:

            if not triple.is_contained_in(self.triples_refinements[-2]):
                return False

        for triple in self.triples_refinements[-2]:

            if not triple.is_contained_in(self.triples_refinements[-1]):
                return False

        return True
