from .cmap_creation_state import CMapCreationState
from llms_kgs.llms import LLMProtocol

class FocusQuestionExtractor:
    """Extracts a focus question from a given chunk."""

    def __init__(self, llm: LLMProtocol, system_prompt: str, user_template: str):
        """Important precondition: user_template has a {text} field."""

        self._llm = llm
        self._system_prompt = system_prompt
        self._user_template = user_template

    def extract(self, creation_state: CMapCreationState):

        prompt = self._user_template.format(text=creation_state.chunk.text.strip())

        llm_invocation = self._llm.call(
            system=self._system_prompt,
            prompt=prompt)

        creation_state.focus_question = llm_invocation.raw_answer
        creation_state.add_invocation(llm_invocation)
