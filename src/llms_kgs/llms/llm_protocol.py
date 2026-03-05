from .llm_invocation_data import LLMInvocationData
from typing import Protocol
import numpy as np

class LLMProtocol(Protocol):
    def call(self, system: str, prompt: str) -> LLMInvocationData:
        ...

    def get_name(self) -> str:
        ...

