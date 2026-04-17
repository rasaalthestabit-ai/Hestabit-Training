from collections import deque
from utils.cleaner import clean_output


class BaseAgent:
    def __init__(self, name, system_prompt, llm):
        self.name = name
        self.system_prompt = system_prompt
        self.llm = llm

        # Separate memory (NOT injected blindly)
        self.chat_logs = deque(maxlen=10)

    def generate(self, input_text):
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": input_text}
        ]

        raw_output = self.llm(messages)

        # ✅ CLEAN OUTPUT (KEY STEP)
        cleaned_output = clean_output(raw_output)

        # ✅ STORE LOGS SEPARATELY
        self.chat_logs.append({
            "input": input_text,
            "raw_output": raw_output,
            "cleaned_output": cleaned_output
        })

        return cleaned_output