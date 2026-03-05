from dataclasses import dataclass

@dataclass
class LLMInvocationData:
    
    execution_time: float = 0
    system_prompt: str = ''
    user_prompt: str = ''
    raw_answer: str = ''
    model_name: str = ''

