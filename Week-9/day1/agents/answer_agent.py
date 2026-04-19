from agents.base_agent import BaseAgent

class AnswerAgent(BaseAgent):
    def __init__(self, llm):
        super().__init__(
            name="AnswerAgent",
            system_prompt="""
            You are an answer agent.
            Your job is to generate a clear final answer for the user.
            Use only the provided summary.
            Be concise and accurate.
            """,
            llm=llm
        )