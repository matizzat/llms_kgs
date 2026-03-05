from llms_kgs.llms import LLMProtocol, LLMInvocationData
from llms_kgs.core_utils import log_error
from llms_kgs.domain import Chunk, Query

from abc import ABC, abstractmethod
from typing import List 


class ABCFormatter(ABC):

    @abstractmethod
    def format_user_prompt(self, query: Query, chunks: List[Chunk]) -> str:
        ...


class PromptFormatter(ABCFormatter):

    def __init__(self, template: str):
        """ Required: template has the fields {chunks} and {query} """

        self._template = template
    
    def format_user_prompt(self, query: Query, chunks: List[Chunk]) -> str:

        chunk_list = '\n'.join(
                [f"[Chunk {i}]\n{chunks[i].text.strip()}\n" for i in range(len(chunks))])

        return self._template.format(chunks = chunk_list, query=query.get())


class Generator:

    def __init__(self, formatter: ABCFormatter, llm: LLMProtocol, system_prompt: str):

        self._system_prompt = system_prompt
        self._formatter = formatter
        self._llm = llm

    def generate(self, query: Query, chunks: List[Chunk]) -> LLMInvocationData:
        
        try:

            user_prompt = self._formatter.format_user_prompt(query, chunks)

            invocation_data = self._llm.call(system = self._system_prompt, prompt = user_prompt)

            return invocation_data

        except Exception as e:

            log_error('Generator', 'generate', e)
            raise RuntimeError(f"generate failed: {e}") from e
