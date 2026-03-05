from llms_kgs.llms import EncoderProtocol, SentenceSplitter 
from llms_kgs.domain import Chunk
import numpy as np

class ChunkEncoder:

    def __init__(self, splitter: SentenceSplitter, ef: EncoderProtocol):

        self._embedding_dimension = ef.get_embedding_dimension() 
        self._max_tokens = ef.get_max_tokens()
        self._splitter = splitter
        self._ef = ef
        
    def encode(self, chunk: Chunk) -> np.ndarray:

        sentences = self._splitter.split(chunk.text)
        if len(sentences) == 0:
            return np.zeros(self._embedding_dimension)

        paragraph = sentences[0] 
        embeddings = []        
        
        for sentence in sentences[1:]:

            combined_text = paragraph + '\n' + sentence

            if(self._ef.count_tokens(combined_text) <= self._max_tokens):
                paragraph = combined_text 
               
            else:
                embeddings.append(self._ef.encode(paragraph))
                paragraph = sentence

        embeddings.append(self._ef.encode(paragraph))

        return np.average(np.array(embeddings), axis=0) 

