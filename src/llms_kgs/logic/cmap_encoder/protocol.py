from typing import Protocol
from llms_kgs.domain import CMap
import numpy as np

class CMapEncoderProtocol(Protocol):
    """
    Protocol definition for Concept Map encoders.
    Any class implementing this protocol must provide an encode 
    method that transforms a CMap into a NumPy vector.
    """

    def encode(self, cmap: CMap) -> np.ndarray:
        """
        Transforms a CMap object into a numerical embedding.

        Args:
            cmap (CMap): The concept map to encode.

        Returns:
            np.ndarray: A vector representation of the knowledge graph.
        """
        ...
