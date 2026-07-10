from .protocol import CMapEncoderProtocol
from llms_kgs.llms import EncoderProtocol
from llms_kgs.domain import CMap
import numpy as np

class CMapQuestionEncoder(CMapEncoderProtocol):
    """
    Computes the embedding for a concept map by using a
    sentence transformer over the focus question.  
    """

    def __init__(self, ef: EncoderProtocol):

        self._ef = ef

    def encode(self, cmap: CMap) -> np.ndarray:

        return self._ef.encode(cmap.focus_question)

