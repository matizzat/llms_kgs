from .llm_invocation_data import LLMInvocationData
from .llm_protocol import LLMProtocol

from typing import Optional, Dict
import ollama
import time
import math

class Gemma3_4B(LLMProtocol):

    def __init__(self, temperature: float = 0.0, schema: Optional[Dict] = None):

       self._temperature = temperature 
       self._schema = schema 


    def call(self, system: str, prompt: str) -> LLMInvocationData:

        def do_call():

            return ollama.generate(
                model='gemma3:4b',
                system=system,
                prompt=prompt,
                format = self._schema,
                options={
                    'temperature': self._temperature,
                    }
                )

        start_t = time.time()
        ans = do_call()
        final_t = time.time() - start_t

        return LLMInvocationData(
                model_name = self.get_name(),
                execution_time = final_t,
                system_prompt = system,
                user_prompt = prompt,
                raw_answer = ans['response'])

    def get_name(self) -> str:
        return 'gemma3:4b'
