from .protocol import CMapEncoderProtocol
from llms_kgs.llms import EncoderProtocol 
from llms_kgs.domain import CMap
import numpy as np

class CMapParagraphEncoder(CMapEncoderProtocol):
    """
    Computes the embedding for a concept map by using a sentence
    transformer over a synthesized text, which is the concatenation
    of the focus question and all the knowledge triples.   

    The text is breaked up into smaller chunks if it surpasses the
    token capacity of the transformer, and the final embedding
    equals the average of the embeddings of the smaller chunks. 
    """
  
    def __init__(self, ef: EncoderProtocol):

        self._max_tokens = ef.get_max_tokens()
        self._ef = ef 

    def encode(self, cmap: CMap) -> np.ndarray:

        paragraph = cmap.focus_question
        embeddings = []  
        
        for triple in cmap.triples:

            sentence = triple.to_sentence()
            combined_text = paragraph + '\n' + sentence

            if(self._ef.count_tokens(combined_text) <= self._max_tokens):

                paragraph = combined_text 

            else: 
                
                embeddings.append(self._ef.encode(paragraph)) 
                paragraph = sentence
       
        embeddings.append(self._ef.encode(paragraph))
       
        embedding = np.average(np.array(embeddings), axis=0)
       
        return embedding

