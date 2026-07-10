from .llm_invocation_data import LLMInvocationData
from .llm_protocol import LLMProtocol
import ollama
import time

from typing import Optional, Dict

class Llama_31_8B(LLMProtocol):

    def __init__(self, temperature: float = 0.0, schema: Optional[Dict] = None):

        self._temperature = temperature
        self._schema = schema

    def call(self, system: str, prompt: str) -> LLMInvocationData:
        
        def do_call():
            return ollama.generate(
                model='llama3.1:8b',
                system=system,
                prompt=prompt,
                format = self._schema,
                options={
                    'temperature': self._temperature,
                    'num_ctx': 2048 # Got 100% GPU usage with this value. 
                }
            )

        start_t = time.time()
        ans = do_call()
        execution_time = time.time() - start_t

        return LLMInvocationData(
                model_name = self.get_name(),
                execution_time = execution_time,
                system_prompt = system,
                user_prompt = prompt,
                raw_answer = ans['response'])

    def get_name(self) -> str:
        return 'llama3.1:8b'
