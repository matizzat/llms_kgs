from llms_kgs.llms import LLMProtocol, LLMInvocationData
from llms_kgs.domain import Query, CMap
from llms_kgs.core_utils import Notification, log_error

from abc import ABC, abstractmethod
from typing import List


class AbstractPromptFormatter(ABC):

    def format_user_prompt(self, query: Query, cmaps: List[CMap]) -> str:
        ...


class PromptFormatter(AbstractPromptFormatter):

    def __init__(self, template: str):
        """ Constraint: template has field {chunks} and {query} """ 

        self._template = template
        
    def format_user_prompt(self, query: Query, cmaps: List[CMap]) -> str:
        
        triples_as_string = ['\n'.join(
            [triple.source.label + ' @ ' + triple.relation.label + ' @ ' + triple.target.label
                for triple in cmap.triples])
            for cmap in cmaps]

        cmaps_as_string = '\n\n'.join([f"Concept Map {i}:\nFocus Question: "
                      f"{cmaps[i].focus_question}\n{triples_as_string[i]}"
                      for i in range(len(cmaps))])

        return self._template.format(
                query = query.text, cmaps = cmaps_as_string)


class Generator:

    def __init__(self, formatter: AbstractPromptFormatter,
            llm: LLMProtocol, system_prompt: str):

        self._formatter = formatter
        self._llm = llm
        self._system_prompt = system_prompt

    def generate(self, query: Query, cmaps: List[CMap]) -> LLMInvocationData:
       
        try:
            
            # Format user prompt:
            user_prompt = self._formatter.format_user_prompt(query, cmaps)

            # Call llm:
            invocation = self._llm.call(
                    system = self._system_prompt, prompt = user_prompt)

            return invocation

        except Exception as e:
           
            log_error('Genreator', 'generate', e)
            raise RuntimeError(f"generate failed: {e}") from e

