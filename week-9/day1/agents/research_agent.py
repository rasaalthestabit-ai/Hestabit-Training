import autogen
from autogen import ConversableAgent

from config import LLM_CONFIG

RESEARCH_SYSTEM_PROMPT = """
You are the Research Agent.

YOUR ONLY JOB:
- Receive a topic or question from the user.
- Return detailed raw research notes.

STRICT RULES:
- Do NOT summarize.
- Do NOT provide a final answer.
- Do NOT include reasoning steps like Thought, Action, or Observation.
- Output only clean research notes.

OUTPUT FORMAT:
- <point 1>
- <point 2>
- <point 3>

End with: [RESEARCH_DONE]
""".strip()

research_agent = ConversableAgent(
    name="ResearchAgent",
    system_message=RESEARCH_SYSTEM_PROMPT,
    llm_config=LLM_CONFIG,
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    silent=True
)