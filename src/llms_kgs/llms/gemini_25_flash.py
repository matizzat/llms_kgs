from .llm_invocation_data import LLMInvocationData
from .llm_protocol import LLMProtocol

from typing import Optional, Dict
from google.genai import types
from google import genai
import time
import math

class Gemini25Flash(LLMProtocol):

    def __init__(self, api_key: Optional[str] = None,
            temperature: float = 0.0, schema: Optional[Dict] = None):

        # Configure client through api key:
        if api_key:
            self._client = genai.Client(api_key=api_key)
        else:
            self._client = genai.Client()

        # Configure the model to generate
        # plain text or structured outputs:  
        if not schema:
            self._response_mime_type = "text/plain"  
        else:
            self._response_mime_type = "application/json"
        
        # Set attributes:
        self._temperature = temperature
        self._schema = schema

    def call(self, system: str, prompt: str) -> LLMInvocationData:

        def do_call():

            return self._client.models.generate_content(

                config=types.GenerateContentConfig(

                    system_instruction = system,
                    temperature = self._temperature,
                    response_mime_type =  self._response_mime_type,
                    response_json_schema = self._schema,
                ),

                model = "gemini-2.5-flash",
                contents = prompt,
            )

        start_t = time.time()
        ans = do_call()
        final_t = time.time() - start_t
        time.sleep(1) # We need it to not exceed the API quota.   

        return LLMInvocationData(
                model_name = self.get_name(),
                execution_time = final_t,
                system_prompt = system,
                user_prompt = prompt,
                raw_answer = ans.text)

    def get_name(self) -> str:
        return 'gemini-2.5-flash'
