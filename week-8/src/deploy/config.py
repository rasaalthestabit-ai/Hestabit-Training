import os

# Base path → src/
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "quantized", "model.gguf")

# -----------------------------
# GENERATION DEFAULTS
# -----------------------------
MAX_TOKENS = 100
TEMPERATURE = 0.7
TOP_P = 0.9
TOP_K = 40

# -----------------------------
# SYSTEM PROMPT
# -----------------------------
SYSTEM_PROMPT = (
    "You are a professional HR assistant.\n"
    "Answer clearly using known HR knowledge.\n"
    "If the question is about a specific company or unknown policy, say 'I don't have that information.'"
)

# -----------------------------
# CHAT MEMORY CONTROL
# -----------------------------
MAX_HISTORY = 3