class RAGEvaluator:
    def __init__(self, llm):
        self.llm = llm

    def hallucination_check(self, context, answer):
        prompt = f"""
Context:
{context}

Answer:
{answer}

Is the answer fully supported by the context?
Reply only YES or NO.
"""
        result = self.llm.generate(prompt)
        return "YES" in result.upper()

    def faithfulness_score(self, context, answer):
        prompt = f"""
    Rate how faithful the answer is to the context (0 to 1).

    ONLY return a number. No explanation.

    Context:
    {context}

    Answer:
    {answer}

    Score:
    """
        score = self.llm.generate(prompt)

        # 🔥 SAFE PARSING
        try:
            return float(score.strip())
        except:
            return 0.0

    def refine_answer(self, context, answer):
        prompt = f"""
    You are a precise assistant.

    Rewrite the answer to be:
    - Short
    - Direct
    - Based on the given data
    - DO NOT add explanations or disclaimers

    Context:
    {context}

    Answer:
    {answer}

    Final Answer:
    """
        return self.llm.generate(prompt)