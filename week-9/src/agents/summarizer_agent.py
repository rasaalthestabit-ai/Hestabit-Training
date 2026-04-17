from .base_agent import BaseAgent
from llm.llm import generate

class SummarizerAgent(BaseAgent):
    def __init__(self):
        system_prompt = """
You are a Summarizer Agent.
You will be given som input text and you have to summarize it into 3-5 lines.
Use bullet points.

Do NOT repeat instructions or add extra text that is irrelevant to the input.

END after summary.
"""
        super().__init__("summarizer_agent", system_prompt, generate)