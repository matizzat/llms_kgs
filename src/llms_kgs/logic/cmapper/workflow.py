from dataclasses import dataclass, field
from llms_kgs.llms import LLMProtocol, LLMInvocationData
from llms_kgs.domain import Chunk, CMap, Triple, Label
from typing import List
import re


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
    focus_question: str = "" 
    concepts: List[Label] = field(default_factory=list)
    relations: List[Label] = field(default_factory=list)
    triples_evolution: List[List[Triple]] = field(default_factory=list)

    # Tracking:  
    llm_invocations: List[LLMInvocationData] = field(default_factory=list)
  
    def add_triples(self, triples: List[Triple]):
        self.triples_evolution.append(triples)

    def add_llm_invocation(self, llm_invocation: LLMInvocationData):
        self.llm_invocations.append(llm_invocation)
  
    def has_converged(self) -> bool:
        """
        Returns True if the triples improvement algorithm reached a fixed point:
        The LLM outputs the same set of triples when asked to
        improve the current concept map.  
        """
        if len(self.triples_evolution) < 2:
            return False

        triples1 = set((t.source.label, t.relation.label, t.target.label) 
                      for t in self.triples_evolution[-1])

        triples2 = set((t.source.label, t.relation.label, t.target.label) 
                      for t in self.triples_evolution[-2])
       
        return triples1 == triples2

    def to_cmap(self, version: int) -> CMap:
        """
        Returns a CMap object with the focus question and the triple
        list number 'version' created during the workflow.
        """

        if version < 0 or version >= len(self.triples_evolution):
            raise RuntimeError("CMap version out of bound")

        return CMap(focus_question = self.focus_question,
                    triples = self.triples_evolution[version])



class ConceptListParser:
    """Parses the LLM answer into a concept list."""

    def __init__(self, concepts_regular_expression: str):
        self._concepts_regular_expression = concepts_regular_expression

    def parse(self, llm_invocation: LLMInvocationData) -> List[Label]:
        return [Label(label) for label in re.findall(
            self._concepts_regular_expression, llm_invocation.raw_answer)]


class RelationListParser:
    """Parses the LLM answer into a relation list."""

    def __init__(self, relations_regular_expression: str):
        self._relations_regular_expression = relations_regular_expression

    def parse(self, llm_invocation: LLMInvocationData) -> List[Label]:
        return [Label(label) for label in re.findall(
            self._relations_regular_expression, llm_invocation.raw_answer)]


class TripleListParser:
    """Parses the LLM answer into a triple list."""

    def __init__(self, triples_regular_expression: str):
        self._triples_regular_expression = triples_regular_expression

    def parse(self, llm_invocation: LLMInvocationData) -> List[Triple]:
        return [Triple(source=s, relation=r, target=t)
                for s, r, t in re.findall(
                    self._triples_regular_expression, 
                    llm_invocation.raw_answer)]


class FocusQuestionExtractor:
    """Extracts a focus question from a given chunk."""

    def __init__(self, llm: LLMProtocol, system_prompt: str, user_template: str):
        """Important precondition: user_template has a {kt} field."""
        self._llm = llm
        self._system_prompt = system_prompt
        self._user_template = user_template

    def extract(self, creation_state: CMapCreationState):
        prompt = self._user_template.format(kt=creation_state.chunk.text) 

        llm_invocation = self._llm.call(
            system=self._system_prompt, 
            prompt=prompt)

        creation_state.focus_question = llm_invocation.raw_answer
        creation_state.add_llm_invocation(llm_invocation)


class ConceptListExtractor:
    """Extracts a concept list from a chunk and a focus question."""

    def __init__(self, llm: LLMProtocol, system_prompt: str, 
                 user_template: str, parser: ConceptListParser):
        """Important precondition: user_template has fields {kt} and {fq}."""
        self._llm = llm
        self._system_prompt = system_prompt
        self._user_template = user_template
        self._parser = parser

    def _format_user_prompt(self, creation_state: CMapCreationState) -> str:
        return self._user_template.format(
            fq=creation_state.focus_question, 
            kt=creation_state.chunk.text)
   
    def extract(self, creation_state: CMapCreationState): 
        prompt = self._format_user_prompt(creation_state)

        llm_invocation = self._llm.call(
            system=self._system_prompt, 
            prompt=prompt)

        creation_state.concepts = self._parser.parse(llm_invocation)
        creation_state.add_llm_invocation(llm_invocation)


class RelationListExtractor:
    """Extracts a relation list from a chunk, a concept list and a focus question."""

    def __init__(self, llm: LLMProtocol, system_prompt: str, 
                 user_template: str, parser: RelationListParser):
        """Important precondition: user_template has fields {kt}, {cs} and {fq}."""
        self._llm = llm
        self._system_prompt = system_prompt
        self._user_template = user_template
        self._parser = parser

    def _format_user_prompt(self, creation_state: CMapCreationState) -> str:
        concept_list_string = "\n".join([concept.label
            for concept in creation_state.concepts])

        return self._user_template.format(
            fq=creation_state.focus_question,
            cs=concept_list_string, 
            kt=creation_state.chunk.text)
  
    def extract(self, creation_state: CMapCreationState):
        prompt = self._format_user_prompt(creation_state)

        llm_invocation = self._llm.call(
            system=self._system_prompt, 
            prompt=prompt)

        creation_state.relations = self._parser.parse(llm_invocation)
        creation_state.add_llm_invocation(llm_invocation)


class TripleListExtractor:
    """
    Extracts a triple list from a given chunk, focus question, concept list
    and relation list. 
    """

    def __init__(self, llm: LLMProtocol, system_prompt: str, 
                 user_template: str, parser: TripleListParser):
        """Important precondition: user_template has fields {kt}, {cs}, {rs} and {fq}."""
        self._llm = llm
        self._system_prompt = system_prompt
        self._user_template = user_template
        self._parser = parser

    def _format_user_prompt(self, creation_state: CMapCreationState) -> str:
        concept_list_string = "\n".join([concept.label
            for concept in creation_state.concepts])
        
        relation_list_string = "\n".join([relation.label
            for relation in creation_state.relations])

        return self._user_template.format(
            fq=creation_state.focus_question,
            cs=concept_list_string, 
            rs=relation_list_string, 
            kt=creation_state.chunk.text)

    def extract(self, creation_state: CMapCreationState):
        prompt = self._format_user_prompt(creation_state)

        llm_invocation = self._llm.call(
            system=self._system_prompt, 
            prompt=prompt)

        creation_state.add_triples(self._parser.parse(llm_invocation))
        creation_state.add_llm_invocation(llm_invocation)


class TripleListImprover:
    """Improves a concept map's triple list created from a given chunk."""

    def __init__(self, llm: LLMProtocol, system_prompt: str, 
                 user_template: str, parser: TripleListParser):
        """Important precondition: user_template has fields {kt}, {ts} and {fq}."""
        self._llm = llm
        self._system_prompt = system_prompt
        self._user_template = user_template
        self._parser = parser

    def _format_user_prompt(self, creation_state: CMapCreationState) -> str:
        # Get the latest triples
        latest_triples = creation_state.triples_evolution[-1]

        triple_list_string = "\n".join([
            "@! " + triple.source.label +
            " @ " + triple.relation.label +
            " @ " + triple.target.label + " !@"
            for triple in latest_triples])

        return self._user_template.format(
            fq=creation_state.focus_question,
            ts=triple_list_string,
            kt=creation_state.chunk.text)

    def improve(self, creation_state: CMapCreationState):
        prompt = self._format_user_prompt(creation_state)

        llm_invocation = self._llm.call(
            system=self._system_prompt, 
            prompt=prompt)

        creation_state.add_triples(self._parser.parse(llm_invocation))
        creation_state.add_llm_invocation(llm_invocation)


class CMapCreationWorkflow:
    """
    Orchestrator of the concept map creation workflow.
    """

    def __init__(self,
            focus_question_extractor: FocusQuestionExtractor,
            concepts_extractor: ConceptListExtractor,
            relations_extractor: RelationListExtractor,
            triples_extractor: TripleListExtractor,
            triples_improver: TripleListImprover): 
                       
        self._focus_question_extractor = focus_question_extractor
        self._concepts_extractor = concepts_extractor
        self._relations_extractor = relations_extractor 
        self._triples_extractor = triples_extractor 
        self._triples_improver = triples_improver 

    def create_cmap(self, chunk: Chunk, max_improvements: int = 0) -> CMapCreationState:
        state = CMapCreationState(chunk)
        
        self._focus_question_extractor.extract(state)
        self._concepts_extractor.extract(state)
        self._relations_extractor.extract(state)
        self._triples_extractor.extract(state)

        for _ in range(max_improvements):
            self._triples_improver.improve(state)

            if state.has_converged(): 
                break 

        return state
