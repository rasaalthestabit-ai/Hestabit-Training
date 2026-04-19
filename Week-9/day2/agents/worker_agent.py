# agents/worker_agent.py

from transformers import pipeline
import wikipedia


class WorkerAgent:
    def __init__(self):
        self.model = pipeline(
            "text-generation",
            model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
            max_new_tokens=200,
            do_sample=False,
            device=-1
        )

    def retrieve(self, query: str) -> str:
        try:
            return wikipedia.summary(query, sentences=2)
        except:
            return ""

    def run(self, task: str) -> str:
        context = self.retrieve(task)

        # 🚨 HARD CONSTRAINT
        prompt = f"""
<|system|>
You must answer ONLY using the given context.

Rules:
- If answer not in context → say "I don't know"
- Do NOT add external knowledge
- Be concise

Context:
{context}

<|user|>
{task}

<|assistant|>
"""
        output = self.model(prompt)[0]["generated_text"]
        return output.split("<|assistant|>")[-1].strip()