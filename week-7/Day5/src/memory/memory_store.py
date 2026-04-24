import json
import os


class MemoryStore:
    def __init__(self, path="src/logs/CHAT-LOGS.json", max_history=5):
        self.path = path
        self.max_history = max_history

        if not os.path.exists(self.path):
            with open(self.path, "w") as f:
                json.dump([], f)

    def load(self):
        with open(self.path, "r") as f:
            return json.load(f)

    def save(self, data):
        with open(self.path, "w") as f:
            json.dump(data, f, indent=2)

    def add(self, user_query, response):
        data = self.load()

        data.append({
            "query": user_query,
            "response": response
        })

        # keep last N messages
        data = data[-self.max_history:]

        self.save(data)

    def get_context(self):
        data = self.load()

        context = ""
        for d in data:
            context += f"User: {d['query']}\n"
            context += f"Assistant: {d['response']}\n"

        return context