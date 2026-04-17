from transformers import pipeline

pipe = pipeline(
    "text-generation",
    model="microsoft/phi-3-mini-4k-instruct",
    device_map="auto"
)

def generate(messages):
    system = ""
    user = ""

    for msg in messages:
        if msg["role"] == "system":
            system = msg["content"]
        elif msg["role"] == "user":
            user = msg["content"]

    prompt = f"""
{system}

### INPUT:
{user}

### OUTPUT:
"""

    output = pipe(
        prompt,
        max_new_tokens=160,
        do_sample=False,
        eos_token_id=pipe.tokenizer.eos_token_id  # ✅ important
    )[0]["generated_text"]

    result = output.replace(prompt, "").strip()

    # ✂️ HARD STOP CLEANING
    result = result.split("###")[0]   # remove leaked sections
    result = result.split("INPUT:")[0]
    result = result.split("Output:")[0]

    return result.strip()