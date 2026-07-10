from llms_kgs.core_utils import Notification
import numpy as np
import re

class Chunk:

    _text_forbidden_substrings = [' @ ']
    _min_title_len = 1
    _min_text_len = 1

    def __init__(self, chunk_id: int = 0, title: str = '', text: str = '', embedding: np.ndarray = np.zeros(1)):
        self.title = self.normalize_title(title)
        self.embedding = embedding
        self.id = chunk_id
        self.text = text

    def normalize_title(self, title: str) -> str:
        normalized = title.strip()
        return normalized

    def is_valid(self, notification: Notification) -> bool:
        result = True

        if(len(self.text) < self._min_text_len):
            notification.add_error(f"Chunk's text must have at least {self._min_text_len} character/s.")
            result = False

        if(len(self.title) < self._min_title_len):
            notification.add_error(f"Chunk's title must have at least {self._min_title_len} character/s.")
            result = False

        for c in self._text_forbidden_substrings:
            if(c in self.text):
                notification.add_error(f"Chunk's text can't contain the substring '{c}'.")
                result = False

        return result

    def to_dict(self) -> dict:
        
        return {
            "id": self.id,
            "title": self.title,
            "text": self.text,
            # Handle numpy array serialization
            "embedding": self.embedding.tolist() if isinstance(self.embedding, np.ndarray) else []
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Chunk':
        return cls(
            chunk_id=data.get("id", 0),
            title=data.get("title", ""),
            text=data.get("text", ""),
            # Convert list back to numpy array
            embedding=np.array(data.get("embedding", []))
        )
