from core.memory import Memory

class BaseAgent:
    def __init__(self, name, system_prompt, llm):
        self.name = name
        self.system_prompt = system_prompt
        self.memory = Memory(max_size=10)
        self.llm = llm

    def receive(self, message):
        self.memory.add(message)

    def clean_output(self, text):
        if "Final Answer:" in text:
            text = text.split("Final Answer:")[-1]

        # Remove system prompt leakage
        text = text.replace(self.system_prompt, "")

        # Remove unwanted tokens
        junk_phrases = [
            "You are a",
            "Context:",
            "Input:",
            "Output:"
        ]

        for phrase in junk_phrases:
            text = text.replace(phrase, "")

        return text.strip()
    
    def think(self, input_text):
        context = self.memory.get_context()

        prompt = f"""
    {self.system_prompt}

    Strict Rules:
    - Do NOT repeat instructions
    - Do NOT include system prompt
    - Do NOT include the word 'Context' or 'Input'
    - ONLY return the final result

    Context:
    {context}

    Input:
    {input_text}

    Final Answer:
    """
        response = self.llm.generate(prompt)

        return self.clean_output(response)

    def act(self, message):
        self.receive(message)
        response = self.think(message.content)
        return response