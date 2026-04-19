from transformers import pipeline

class LLM:
    def __init__(self, model_name="TinyLlama/TinyLlama-1.1B-Chat-v1.0"):
        self.pipe = pipeline("text-generation", model=model_name, temperature=0.3, return_full_text=False)

    def generate(self, prompt):
        response = self.pipe(prompt, max_new_tokens=200)[0]["generated_text"]
        return response