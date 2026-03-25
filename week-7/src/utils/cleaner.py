import re

def clean_text(text):
    # Normalize newlines first
    text = re.sub(r'\n+', '\n', text)

    # Normalize spaces (but keep newlines)
    text = re.sub(r'[ \t]+', ' ', text)

    return text.strip()