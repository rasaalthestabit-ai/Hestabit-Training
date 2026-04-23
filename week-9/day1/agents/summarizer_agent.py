import autogen
from autogen import ConversableAgent

from config import LLM_CONFIG

SUMMARIZER_SYSTEM_PROMPT = """
You are the Summarizer Agent.

YOUR ONLY JOB:
- Convert research notes into a concise summary.

STRICT RULES:
- Do NOT add new information.
- Do NOT include reasoning steps (no Thought/Action/Observation).
- Output only 3-5 bullet points.

OUTPUT FORMAT:
• <point 1>
• <point 2>
• <point 3>

End with: [SUMMARY_DONE]
""".strip()

summarizer_agent = ConversableAgent(
    name="SummarizerAgent",
    system_message=SUMMARIZER_SYSTEM_PROMPT,
    human_input_mode="NEVER",
    llm_config=LLM_CONFIG,
    max_consecutive_auto_reply=10,
    silent=True
)