from .base_agent import BaseAgent
from llm.llm import generate

class AnswerAgent(BaseAgent):
    def __init__(self):
        system_prompt = """
You are an Answer Agent.
You will be given some input and you have to return a final answer.

Do NOT include instructions or include extra sections.

END after answer.
"""
        super().__init__("answer_agent", system_prompt, generate)