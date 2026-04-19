from core.llm import LLM
from core.message import Message
from agents.research_agent import ResearchAgent
from agents.summarizer_agent import SummarizerAgent
from agents.answer_agent import AnswerAgent

llm = LLM()

research_agent = ResearchAgent(llm)
summarizer_agent = SummarizerAgent(llm)
answer_agent = AnswerAgent(llm)

user_query = "Explain quantum computing"

# Step 1 → Research
msg1 = Message("User", "ResearchAgent", user_query)
research_output = research_agent.act(msg1)

msg2 = Message(
    "ResearchAgent",
    "SummarizerAgent",
    research_output.strip()
)

summary = summarizer_agent.act(msg2)

msg3 = Message(
    "SummarizerAgent",
    "AnswerAgent",
    summary.strip()
)
final_answer = answer_agent.act(msg3)

print(final_answer)