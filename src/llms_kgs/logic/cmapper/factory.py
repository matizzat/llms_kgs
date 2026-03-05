#cmapper/factory.py

from .workflow import (
    ConceptListParser, RelationListParser, TripleListParser,
    FocusQuestionExtractor, ConceptListExtractor, RelationListExtractor,
    TripleListExtractor, TripleListImprover, CMapCreationWorkflow
)

from .prompts import (
    LABEL_LIST_PATTERN, TRIPLE_LIST_PATTERN,
    FOCUS_QUESTION_SYSTEM, FOCUS_QUESTION_USER,
    CONCEPTS_SYSTEM, CONCEPTS_USER,
    RELATIONS_SYSTEM, RELATIONS_USER,
    TRIPLES_SYSTEM, TRIPLES_USER,
    IMPROVE_TRIPLES_SYSTEM, IMPROVE_TRIPLES_USER
)

from llms_kgs.llms import LLMProtocol

class WorkflowFactory:
    """
    Orchestrates the creation of default CMapCreationWorkflow objects.
    """

    @staticmethod
    def create_default(llm: LLMProtocol) -> CMapCreationWorkflow:
        """
        Creates a workflow configured with the recommended regex 
        patterns and system prompts.
        """
        # Initialize Parsers:
        concept_parser = ConceptListParser(LABEL_LIST_PATTERN)
        relation_parser = RelationListParser(LABEL_LIST_PATTERN)
        triple_parser = TripleListParser(TRIPLE_LIST_PATTERN)

        # Initialize Extractors:
        fq_extractor = FocusQuestionExtractor(
            llm=llm,
            system_prompt=FOCUS_QUESTION_SYSTEM,
            user_template=FOCUS_QUESTION_USER
        )

        concepts_extractor = ConceptListExtractor(
            llm=llm,
            system_prompt=CONCEPTS_SYSTEM,
            user_template=CONCEPTS_USER,
            parser=concept_parser
        )

        relations_extractor = RelationListExtractor(
            llm=llm,
            system_prompt=RELATIONS_SYSTEM,
            user_template=RELATIONS_USER,
            parser=relation_parser
        )

        triples_extractor = TripleListExtractor(
            llm=llm,
            system_prompt=TRIPLES_SYSTEM,
            user_template=TRIPLES_USER,
            parser=triple_parser
        )

        triples_improver = TripleListImprover(
            llm=llm,
            system_prompt=IMPROVE_TRIPLES_SYSTEM,
            user_template=IMPROVE_TRIPLES_USER,
            parser=triple_parser
        )

        # Return the workflow:
        return CMapCreationWorkflow(
            focus_question_extractor=fq_extractor,
            concepts_extractor=concepts_extractor,
            relations_extractor=relations_extractor,
            triples_extractor=triples_extractor,
            triples_improver=triples_improver
        )
