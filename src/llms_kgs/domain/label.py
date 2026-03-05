from llms_kgs.core_utils import Notification

from typing import List

class Label:

    forbidden_substrings = [' @ ']
    min_len = 1
    
    def __init__(self, label: str):
        self.label = Label.normalize(label)
   
    @staticmethod
    def normalize(label: str) -> str:

        for c in Label.forbidden_substrings:
            label = label.replace(c, '')

        label = label.strip()
        label = " ".join(label.split())
        
        return label

    def is_valid(self, notif: Notification) -> bool:

        result = True

        if(len(self.label) < Label.min_len):
            notif.add_error(f"Label \"{self.label}\" must have at least {self._min_len} character/s.")
            result = False 

        for c in self._forbidden_substrings:

            if(c in self.label):

                notif.add_error(f"Label \"{self.label}\" can't contain substring \"{c}\".")
                result = False

        return result 

    def equal_to(self, target: 'Label') -> bool:

        if(Label.normalize(self.label) == 
                Label.normalize(target.label)):

            return True
        
        return False

    def is_contained_in(self, labels: List['Label']) -> bool:

        for label in labels:

            if self.equal_to(label):
                return True
        
        return False

    def to_dict(self) -> dict:
        return {"label": self.label}

    @classmethod
    def from_dict(cls, data: dict) -> 'Label':
        return cls(label=data.get("label", ""))

