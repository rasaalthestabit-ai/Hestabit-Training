from agents.base_agent import BaseAgent

class SummarizerAgent(BaseAgent):
    def __init__(self, llm):
        super().__init__(
            name="SummarizerAgent",
            system_prompt="""
            You are a summarizer agent.
            Your job is to condense information.
            Keep key points only.
            Do NOT add new information.
            """,
            llm=llm
        )