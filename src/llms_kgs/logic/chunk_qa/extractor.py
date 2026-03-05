from pydantic import BaseModel
from typing import List, Tuple

from llms_kgs.llms import LLMProtocol, LLMInvocationData
from .prompts import EXTRACTOR_SYSTEM_TEMPLATE

class AnnotatedPassage(BaseModel):

    text: str
    chunk_number: int

class Answer(BaseModel):

    passages: List[AnnotatedPassage]
    final_answer: str

class Extractor:

    def __init__(self, llm: LLMProtocol):
        """ Prerrequisite: llm output schema equals 'Answer' schema. """

        self._llm = llm
        

    def extract(self, text: str) -> Tuple[LLMInvocationData, Answer]:

        try:

            # Format system prompt:
            system_prompt = EXTRACTOR_SYSTEM_TEMPLATE.format(
                    schema = Answer.model_json_schema())

            # Call LLM:
            invocation = self._llm.call(system=system_prompt, prompt=text)

            # Parse raw answer as an 'AnswerComponents' object: 
            answer_components = Answer.model_validate_json(invocation.raw_answer)

            return invocation, answer_components 

        except Exception as e:

            log_error('Extractor', 'extract', e)
            raise RuntimeError(f"extract failed: {e}") from e
