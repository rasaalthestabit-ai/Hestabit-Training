import autogen
from autogen import ConversableAgent

from config import LLM_CONFIG

ANSWER_SYSTEM_PROMPT = """
You are the Answer Agent.

YOUR ONLY JOB:
- Convert the summary into a clear final answer.

STRICT RULES:
- Do NOT include reasoning steps.
- Do NOT include Thought, Action, or Observation.
- Write a clean, user-friendly answer.

OUTPUT:
<final answer>

End with: [ANSWER_DONE]
""".strip()

answer_agent = ConversableAgent(
    name="AnswerAgent",
    system_message=ANSWER_SYSTEM_PROMPT,
    llm_config=LLM_CONFIG,
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    silent=True
)