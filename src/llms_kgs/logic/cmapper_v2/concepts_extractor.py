from .parsing_model import ConceptList
from .cmap_creation_state import CMapCreationState

from llms_kgs.llms import LLMProtocol


class ConceptsExtractor:
    """Extracts a concept list from a given focus question and chunk."""

    def __init__(self,
            generator_llm: LLMProtocol,
            parser_llm: LLMProtocol,
            generator_system_prompt: str,
            generator_user_template: str,
            parser_system_template: str):

        """Important precondition: user_template has fields {text} and {focus_question}."""

        self._generator_llm = generator_llm
        self._parser_llm = parser_llm
        self._generator_system_prompt = generator_system_prompt
        self._generator_user_template = generator_user_template
        self._parser_system_template = parser_system_template

    def extract(self, creation_state: CMapCreationState):

        # Format concept list generation user prompt: 
        generator_prompt = self._generator_user_template.format(
                focus_question = creation_state.focus_question,
                text=creation_state.chunk.text.strip())

        # Call concept list generator:
        generator_invocation = self._generator_llm.call(
            system = self._generator_system_prompt,
            prompt = generator_prompt)

        # Format parser system prompt:
        parser_system_prompt = self._parser_system_template.format(
                schema = ConceptList.model_json_schema())

        # Call concept list parser:
        parser_invocation = self._parser_llm.call(
            system = parser_system_prompt,
            prompt = generator_invocation.raw_answer)

        # Parse json as ConceptList object:
        concept_list = ConceptList.model_validate_json(parser_invocation.raw_answer)

        # Update state:
        creation_state.add_invocation(generator_invocation)
        creation_state.add_invocation(parser_invocation)
      
        creation_state.concepts = concept_list.concepts
