from .base_agent import BaseAgent
from llm.llm import generate

class ResearchAgent(BaseAgent):
    def __init__(self):
        system_prompt = """
You are a Research Agent.

Return ONLY bullet points.

Do NOT:
- repeat instructions
- include anything after output

END your response after bullet points.
"""
        super().__init__("research_agent", system_prompt, generate)