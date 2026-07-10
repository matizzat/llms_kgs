from llms_kgs.core_utils import Notification
from .triple import Triple
from typing import List
import numpy as np
import re

class CMap:

    _fq_forbidden_substrings = [' @ ']

    def __init__(self, cmap_id: int = 0, title: str = '', focus_question: str = '',
            triples: List[Triple] = [], embedding: np.ndarray = np.zeros(1)):
    
        self.focus_question = self.normalize_focus_question(focus_question)
        self.title = self.normalize_title(title)
        self.embedding = embedding
        self.triples = triples 
        self.id = cmap_id

    def normalize_focus_question(self, focus_question: str) -> str:
        
        return focus_question.strip()

    def normalize_title(self, title: str) -> str:
        
        return title.strip() 

    def is_valid(self, notification: Notification) -> bool:
        result = True

        if(len(self.title) == 0):

            notification.add_error(f'CMap title must have at least 1 character.')
            result = False

        if(len(self.focus_question) == 0):
            
            notification.add_error(f"CMap focus question must have at least 1 character.")
            result = False 

        for c in self._fq_forbidden_substrings:

            if c in self.focus_question:

                notification.add_error(f"CMap focus question can't contain the substring '{c}'.")
                result = False

        for triple in self.triples:

            if not triple.is_valid(notification):
                result = False
        
        return result

    def has_triple(self, triple: Triple) -> bool:

        for my_triple in self.triples: 

            if my_triple.equal_to(triple):
                return True

        return False

    def has_triples(self, triples: List[Triple]) -> bool:
        
        for triple in triples:

            if(self.has_triple(triple) == False):
                return False

        return True

    def to_dict(self) -> dict:

        return {
            "id": self.id,
            "title": self.title,
            "focus_question": self.focus_question,
            "triples": [t.to_dict() for t in self.triples],
            "embedding": self.embedding.tolist() if isinstance(self.embedding, np.ndarray) else []
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'CMap':

        # Reconstruct Domain Triples
        triples_data = data.get("triples", [])
        reconstructed_triples = [Triple.from_dict(t) for t in triples_data]

        return cls(
            cmap_id=data.get("id", 0),
            title=data.get("title", ""),
            focus_question=data.get("focus_question", ""),
            triples=reconstructed_triples,
            embedding=np.array(data.get("embedding", []))
        )
