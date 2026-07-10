from typing import Protocol
import numpy as np

class EncoderProtocol(Protocol):
    def encode(self, text: str) -> np.ndarray:
        ... 

    def count_tokens(self, text: str) -> int:
        ...
    
    def get_embedding_dimension(self) -> int:
        ... 
    
    def get_max_tokens(self) -> int:
        ...

