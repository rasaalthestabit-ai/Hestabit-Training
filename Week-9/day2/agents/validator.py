# agents/validator.py

class Validator:
    def run(self, text: str) -> str:
        if "I don't know" in text:
            return "UNCERTAIN"

        if len(text.strip()) < 15:
            return "INVALID"

        return text