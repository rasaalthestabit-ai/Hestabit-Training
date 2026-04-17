import re

def clean_output(text: str) -> str:
    if not text:
        return ""

    # Remove system prompt leakage
    text = re.sub(r"You are .*?Agent\.", "", text)

    # Remove role labels
    text = re.sub(r"(User:|Assistant:|agent:)", "", text)

    # Remove repeated instructions
    text = re.sub(r"TASK:.*?RULES:.*?", "", text, flags=re.DOTALL)

    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()