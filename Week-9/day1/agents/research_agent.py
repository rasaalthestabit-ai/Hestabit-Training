from agents.base_agent import BaseAgent

class ResearchAgent(BaseAgent):
    def __init__(self, llm):
        super().__init__(
            name="ResearchAgent",
            system_prompt="""
            You are a research agent.
            Your job is to gather factual, detailed information.
            DO NOT summarize.
            DO NOT answer the user directly.
            ONLY provide raw researched information.
            """,
            llm=llm
        )