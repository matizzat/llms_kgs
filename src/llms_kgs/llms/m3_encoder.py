from .encoder_protocol import EncoderProtocol 
from FlagEmbedding import BGEM3FlagModel
import numpy as np
import os

class M3Encoder(EncoderProtocol):

    def __init__(self):
        # Gets the directory where class.py is located:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(current_dir, 'bge-m3-local')

        self._ef = BGEM3FlagModel(model_path, use_fp16=False)

        # Cache the embedding dimension
        self._embedding_dim = 1024

    def count_tokens(self, sentence: str) -> int:
        tok = self._ef.tokenizer
        aux = tok.encode(sentence)
        return len(aux)
    
    def get_max_tokens(self) -> int:
        return self._ef.passage_max_length

    def encode(self, sentence: str) -> np.ndarray:
        aux = self._ef.encode(sentence,
                             max_length = self._ef.passage_max_length)
        
        # Ensure we return a numpy array
        embedding = aux['dense_vecs']
        if not isinstance(embedding, np.ndarray):
            return np.array(embedding)
        return embedding

    def get_embedding_dimension(self) -> int:
        return self._embedding_dim
