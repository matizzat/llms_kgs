from llms_kgs.core_utils import Notification
from .label import Label

from typing import List
import numpy as np


class Triple:

    def __init__(self, source: str, relation: str, target: str, embedding: np.ndarray = np.zeros(1)):

        self.relation: Label = Label(relation)
        self.source: Label = Label(source)
        self.target: Label = Label(target)
        self.embedding: np.ndarray = embedding

    def to_sentence(self) -> str:
        return self.source.label + ' ' + self.relation.label + ' ' + self.target.label

    def is_valid(self, notification: Notification) -> bool:

        return (self.source.is_valid(notification) and 
                self.target.is_valid(notification) and self.relation.is_valid(notification))

    def equal_to(self, triple: 'Triple') -> bool: 
        
        if (triple.relation.equal_to(self.relation) and
            triple.source.equal_to(self.source)     and
            triple.target.equal_to(self.target)):
        
            return True

        return False

    def is_contained_in(self, triples: List['Triple']) -> bool:

        for triple in triples:
            if self.equal_to(triple):
                return True

        return False

    def to_dict(self) -> dict:
        return {
            "source": self.source.to_dict(),
            "relation": self.relation.to_dict(),
            "target": self.target.to_dict(),
            "embedding": self.embedding.tolist() if isinstance(self.embedding, np.ndarray) else []
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Triple':
        return cls(
            source=data.get("source", {}).get("label", ""),
            relation=data.get("relation", {}).get("label", ""),
            target=data.get("target", {}).get("label", ""),
            embedding=np.array(data.get("embedding", []))
            )

