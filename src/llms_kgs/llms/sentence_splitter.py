from typing import List 
import spacy

class SentenceSplitter:
    def __init__(self):
        self._nlp = spacy.load("en_core_web_trf")

    def split(self, text: str) -> List[str]:
        return [str(sentence) for sentence in self._nlp(text).sents]
