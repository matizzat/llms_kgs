from llms_kgs.llms import EncoderProtocol, LLMInvocationData 
from llms_kgs.core_utils import log_error, Notification
from llms_kgs.persistence import ChunkRepository
from llms_kgs.domain import Query, Chunk

from .extractor import Extractor, Answer
from .generator import Generator

from dataclasses import asdict, dataclass, field
from typing import List, Optional


@dataclass
class ChunkQAResult:

    extractor_invocation: LLMInvocationData = field(default_factory=LLMInvocationData)
    generator_invocation: LLMInvocationData = field(default_factory=LLMInvocationData)
    reader_result: Optional[Answer] = None
    notification: Notification = field(default_factory=Notification)
    retrieved_chunks: List[Chunk] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Converts the entire result tree into a JSON-serializable dictionary."""
       
        return {
            # Serialize Dataclasses
            "extractor_invocation": asdict(self.extractor_invocation),
            "generator_invocation": asdict(self.generator_invocation),
           
            # Serialize Pydantic model
            "reader_result": self.reader_result.model_dump() if self.reader_result else None,
           
            # Serialize Custom Classes
            "notification": self.notification.to_dict(),
            "retrieved_chunks": [chunk.to_dict() for chunk in self.retrieved_chunks]
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'ChunkQAResult':
        """Reconstructs the object tree from a dictionary."""
        
        # 1. Reconstruct Dataclasses
        # We unwrap the dictionary (**dict) into the dataclass constructor
        ext_inv = LLMInvocationData(**data.get("extractor_invocation", {}))
        gen_inv = LLMInvocationData(**data.get("generator_invocation", {}))

        # 2. Reconstruct Pydantic Model
        reader_data = data.get("reader_result")
        reader_res = Answer.model_validate(reader_data) if reader_data else None

        # 3. Reconstruct Custom Classes
        notif = Notification.from_dict(data.get("notification", {}))
        chunks = [Chunk.from_dict(c) for c in data.get("retrieved_chunks", [])]

        return cls(
            extractor_invocation=ext_inv,
            generator_invocation=gen_inv,
            reader_result=reader_res,
            notification=notif,
            retrieved_chunks=chunks
        )

class ChunkQALogic:

    def __init__(self, retriever: ChunkRepository, generator: Generator,
            extractor: Extractor, ef: EncoderProtocol):

        self._retriever = retriever 
        self._generator = generator
        self._extractor = extractor
        self._ef = ef

    def k_is_valid(self, k: int, notification: Notification):

        if(k <= 0):
            notification.add_error('Number of neighbors must be a positive number.')

    def answer_query(self, query: str, k: int) -> ChunkQAResult:

        result = ChunkQAResult(notification = Notification())
        
        try:
           
            query = Query(query) 
            
            query.is_valid(result.notification)
            self.k_is_valid(k, result.notification)
           
            if(result.notification.has_errors()):
                return result 

            query_embedding = self._ef.encode(query.text)
            result.retrieved_chunks = self._retriever.retrieve_by_similarity(query_embedding, k) 
            result.generator_invocation = self._generator.generate(query, result.retrieved_chunks)
            result.extractor_invocation, result.reader_result = self._extractor.extract(result.generator_invocation.raw_answer)

        except Exception as e: 

            log_error('ChunkQALogic', 'answer_query', e)
            result.notification.add_error("An unexpected error ocurred. See log for more details.")

        return result 
