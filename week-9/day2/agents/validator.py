from config import call_llm

class ValidatorAgent:
    def validate(self, query: str, answer: str) -> dict:
        prompt = (
            f"You are a validator. Check if this answer properly addresses the query.\n\n"
            f"Query: {query}\n\n"
            f"Answer: {answer}\n\n"
            f"If the answer is good, reply: PASSED\n"
            f"If there are issues, reply: FAILED: <reason>, then write a corrected answer.\n"
        )

        result = call_llm(prompt, max_tokens=300, temperature=0.2)

        if result.upper().startswith("PASSED"):
            return {"passed": True, "answer": answer}
        else:
            lines = result.split("\n", 1)
            corrected = lines[1].strip() if len(lines) > 1 else answer
            return {"passed": False, "answer": corrected or answer}