from .generator import Generator
from .extractor import Extractor, Answer

from llms_kgs.llms import LLMInvocationData, EncoderProtocol
from llms_kgs.core_utils import log_error, Notification
from llms_kgs.persistence import CMapRetriever 
from llms_kgs.domain import Triple, CMap, Query

from dataclasses import asdict, dataclass, field
from typing import List, Optional


@dataclass
class CMapQAResult:
    
    notification: Notification = field(default_factory=Notification)
   
    retrieved_cmaps: List[CMap] = field(default_factory=list)
    
    generator_invocation: LLMInvocationData = field(default_factory=LLMInvocationData)
    extractor_invocation: LLMInvocationData = field(default_factory=LLMInvocationData)

    answer: Optional[Answer] = None

    def to_dict(self) -> dict:
        return {
            "notification": self.notification.to_dict(), 
            "retrieved_cmaps": [cmap.to_dict() for cmap in self.retrieved_cmaps],

            # Dataclasses
            "generator_invocation": asdict(self.generator_invocation),
            "extractor_invocation": asdict(self.extractor_invocation),

            # Pydantic Model (Answer)
            "answer": self.answer.model_dump() if self.answer else None
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'CMapQAResult':

        # 1. Reconstruct Custom Classes
        notif = Notification.from_dict(data.get("notification", {}))
        cmaps = [CMap.from_dict(c) for c in data.get("retrieved_cmaps", [])]

        # 2. Reconstruct Dataclasses
        gen_inv = LLMInvocationData(**data.get("generator_invocation", {}))
        ext_inv = LLMInvocationData(**data.get("extractor_invocation", {}))

        # 3. Reconstruct Pydantic Model
        ans_data = data.get("answer")
        ans_obj = Answer.model_validate(ans_data) if ans_data else None

        return cls(
            notification=notif,
            retrieved_cmaps=cmaps,
            generator_invocation=gen_inv,
            extractor_invocation=ext_inv,
            answer=ans_obj
        )


class CMapQALogic:

    def __init__(self, retriever: CMapRetriever, generator: Generator,
            extractor: Extractor, ef: EncoderProtocol):
        
        self._retriever = retriever 
        self._generator = generator
        self._extractor = extractor
        self._ef = ef 

    def k_is_valid(self, k: int, notification: Notification):
        
        if(k <= 0):
            notification.add_error('Number of neighbors must be a positive number.')

    def answer_query(self, query_str: str, k: int) -> CMapQAResult:

        result = CMapQAResult(notification = Notification()) 

        try:

            query = Query(query_str) 

            query.is_valid(result.notification) 
            self.k_is_valid(k, result.notification)
            
            if(result.notification.has_errors()):
                return result 

            # Compute query embedding:
            query_embedding = self._ef.encode(query.text)

            # Retrieve similar cmaps:
            result.retrieved_cmaps = self._retriever.retrieve_by_similarity(query_embedding, k)

            # Generate answer:
            result.generator_invocation = self._generator.generate(query, result.retrieved_cmaps)

            # Parse answer:
            result.extractor_invocation, result.answer = self._extractor.extract(result.generator_invocation.raw_answer)

        except Exception as e:

            log_error('CMapQALogic', 'answer_query', e)
            result.notification.add_error("An unexpected error ocurred. See log for more details.")

        return result 
