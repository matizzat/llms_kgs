# cmapper_v2/parsing_model.py

from pydantic import BaseModel
from typing import List

class ConceptList(BaseModel):
    concepts: List[str]

class RelationList(BaseModel):
    relations: List[str]

class Triple(BaseModel):
    source: str
    relation: str
    target: str

class TripleList(BaseModel):
    triples: List[Triple]

