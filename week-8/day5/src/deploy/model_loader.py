from llama_cpp import Llama
from .config import MODEL_PATH

print(f"📦 Loading model from: {MODEL_PATH}")

# Load once (global)
llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=512,          # keep stable for your system
    n_threads=4,        # reduce to 2 if CPU struggles
    n_gpu_layers=0
)

def generate_text(prompt, max_tokens, temperature, top_p, top_k):
    try:
        output = llm(
            prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            stop=["USER:", "ASSISTANT:"]
        )
        return output["choices"][0]["text"]

    except Exception as e:
        return f"Error: {str(e)}"