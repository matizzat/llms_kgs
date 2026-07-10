from .prompts import EXTRACTOR_SYSTEM_TEMPLATE

from llms_kgs.llms import LLMProtocol, LLMInvocationData
from llms_kgs.domain import Triple as DomainTriple

from typing import Tuple, List, Dict
from pydantic import BaseModel


""" Anemic domain model for extraction """


class Triple(BaseModel):
    
    source: str
    relation: str
    target: str


class Answer(BaseModel):

    triples: List[Triple]
    final_answer: str

    def domain_triples(self) -> List[DomainTriple]:
        """ Maps anemic model to domain model """

        if not self.triples:
            return []

        return [DomainTriple(t.source, t.relation, t.target)
                for t in self.triples] 

""" Main class """ 


class Extractor:

    def __init__(self, llm: LLMProtocol):
        """ Constraint: llm schema is set to Answer.model_json_schema() """

        self._llm = llm

    def extract(self, text: str) -> Tuple[LLMInvocationData, Answer]:

        # Format prompt:
        system_prompt = EXTRACTOR_SYSTEM_TEMPLATE.format(
                schema=Answer.model_json_schema())

        # Call llm:
        invocation = self._llm.call(system=system_prompt, prompt=text)

        # Parse answer:
        answer = Answer.model_validate_json(invocation.raw_answer)

        return invocation, answer 


