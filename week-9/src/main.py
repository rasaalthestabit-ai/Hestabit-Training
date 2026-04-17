from agents.research_agent import ResearchAgent
from agents.summarizer_agent import SummarizerAgent
from agents.answer_agent import AnswerAgent


# -----------------------------
# CLEANING FUNCTION
# -----------------------------
def clean_text(text: str) -> str:
    """
    Cleans LLM output:
    - Removes extra newlines
    - Removes unwanted role tokens
    - Strips whitespace
    """
    if not text:
        return ""

    text = text.replace("\n", " ")
    text = text.replace("assistant:", "")
    text = text.replace("user:", "")
    text = text.replace("system:", "")
    return text.strip()


# -----------------------------
# DEBUG PRINT HELPER
# -----------------------------
def print_section(title: str, content: str):
    print("\n" + "=" * 50)
    print(f"[{title}]")
    print("=" * 50)
    print(content)


# -----------------------------
# PIPELINE
# -----------------------------
def run_pipeline(query: str):
    # Initialize agents
    research_agent = ResearchAgent()
    summarizer_agent = SummarizerAgent()
    answer_agent = AnswerAgent()

    print_section("USER QUERY", query)

    # -----------------------------
    # STEP 1 → RESEARCH
    # -----------------------------
    research_raw = research_agent.generate(query)
    research_output = clean_text(research_raw)

    print_section("RESEARCH OUTPUT (CLEANED)", research_output)

    # -----------------------------
    # STEP 2 → SUMMARIZE
    # -----------------------------
    summary_raw = summarizer_agent.generate(research_output)
    summary = clean_text(summary_raw)

    print_section("SUMMARY (CLEANED)", summary)

    # -----------------------------
    # STEP 3 → FINAL ANSWER
    # -----------------------------
    final_raw = answer_agent.generate(summary)
    final_answer = clean_text(final_raw)

    print_section("FINAL ANSWER (CLEANED)", final_answer)


# -----------------------------
# ENTRY POINT
# -----------------------------
if __name__ == "__main__":
    while True:
        user_query = input("\nEnter your query (or type 'exit'): ")

        if user_query.lower() == "exit":
            print("Exiting...")
            break

        run_pipeline(user_query)