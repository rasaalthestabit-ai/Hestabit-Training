from fastapi import FastAPI
from pydantic import BaseModel
import uuid
import time

from .model_loader import generate_text
from .config import *

app = FastAPI()

# -----------------------------
# REQUEST MODELS
# -----------------------------
class GenerateRequest(BaseModel):
    prompt: str
    max_tokens: int = MAX_TOKENS
    temperature: float = TEMPERATURE
    top_p: float = TOP_P
    top_k: int = TOP_K


class ChatRequest(BaseModel):
    message: str
    history: list = []
    system_prompt: str = SYSTEM_PROMPT
    max_tokens: int = MAX_TOKENS
    temperature: float = TEMPERATURE
    top_p: float = TOP_P
    top_k: int = TOP_K


# -----------------------------
# RAG PLACEHOLDER (FUTURE)
# -----------------------------
def retrieve_context(query):
    return ""


# -----------------------------
# TASK DETECTION
# -----------------------------
def is_extraction_task(text):
    keywords = ["extract", "structured", "json"]
    return any(k in text.lower() for k in keywords)


# -----------------------------
# HISTORY FILTERING
# -----------------------------
def filter_history(history, current_input):
    filtered = []

    current_is_extraction = is_extraction_task(current_input)

    for turn in history:
        content = turn.get("content", "")

        # detect JSON-like outputs
        is_json = "{" in content and "}" in content

        if current_is_extraction and is_json:
            filtered.append(turn)
        elif not current_is_extraction and not is_json:
            filtered.append(turn)

    return filtered[-MAX_HISTORY:]


# -----------------------------
# PROMPT BUILDER
# -----------------------------
def build_chat_prompt(system_prompt, history, user_input):
    prompt = system_prompt + "\n\n"

    # 🔥 Mode instruction (VERY IMPORTANT)
    if is_extraction_task(user_input):
        prompt += "Respond ONLY in JSON format.\n\n"
    else:
        prompt += "Respond in natural language. Do NOT return JSON.\n\n"

    # 🔥 Few-shot QA
    prompt += (
        "USER: What is attendance policy?\n"
        "ASSISTANT: Attendance policy refers to guidelines for employee presence, punctuality, and work hours.\n\n"
    )

    # 🔥 Few-shot extraction
    if is_extraction_task(user_input):
        prompt += (
            "USER: Extract name, role, company, years from:\n"
            "Amit worked as a Data Analyst at Infosys for 3 years.\n"
            "ASSISTANT: {\"name\":\"Amit\",\"role\":\"Data Analyst\",\"company\":\"Infosys\",\"years\":3}\n\n"
        )
        prompt += (
            "USER: Extract name, role, company from:\n"
            "Rahul worked at Google.\n"
            "ASSISTANT: {\"name\":\"Rahul\",\"role\":null,\"company\":\"Google\"}\n\n"
        )

    # Add filtered history
    for turn in history:
        prompt += f"{turn['role'].upper()}: {turn['content']}\n"

    prompt += f"USER: {user_input}\nASSISTANT:"

    return prompt


# -----------------------------
# ROUTES
# -----------------------------
@app.post("/generate")
def generate(req: GenerateRequest):
    request_id = str(uuid.uuid4())
    start = time.time()

    output = generate_text(
        req.prompt,
        req.max_tokens,
        req.temperature,
        req.top_p,
        req.top_k
    )

    latency = round(time.time() - start, 2)

    print(f"[{request_id}] /generate | latency={latency}s")

    return {
        "request_id": request_id,
        "response": output.strip(),
        "latency": latency
    }


@app.post("/chat")
def chat(req: ChatRequest):
    request_id = str(uuid.uuid4())
    start = time.time()

    context = retrieve_context(req.message)

    # -----------------------------
    # TASK-AWARE SYSTEM PROMPT
    # -----------------------------
    if is_extraction_task(req.message):
        system_prompt = (
    "You are an information extraction system.\n"
    "Extract ONLY the information present in the text.\n"
    "Do NOT guess or infer missing values.\n"
    "If a field is missing, return null.\n"
    "Return ONLY valid JSON.\n"
)
    else:
        system_prompt = req.system_prompt

    # -----------------------------
    # HISTORY FILTERING + TASK SWITCH RESET
    # -----------------------------
    filtered_history = filter_history(req.history, req.message)

    if req.history:
        last_user_msg = req.history[-1].get("content", "")
        if is_extraction_task(last_user_msg) != is_extraction_task(req.message):
            filtered_history = []

    # -----------------------------
    # BUILD PROMPT
    # -----------------------------
    prompt = build_chat_prompt(
        system_prompt + "\n" + context,
        filtered_history,
        req.message
    )

    # -----------------------------
    # GENERATE
    # -----------------------------
    output = generate_text(
        prompt,
        req.max_tokens,
        req.temperature,
        req.top_p,
        req.top_k
    )

    clean_output = output.split("USER:")[0].strip()

    # -----------------------------
    # JSON ENFORCEMENT (EXTRACTION)
    # -----------------------------
    if is_extraction_task(req.message):
        start_idx = clean_output.find("{")
        end_idx = clean_output.rfind("}")

        if start_idx != -1 and end_idx != -1:
            clean_output = clean_output[start_idx:end_idx + 1]

    latency = round(time.time() - start, 2)

    print(f"[{request_id}] /chat | latency={latency}s")

    return {
        "request_id": request_id,
        "response": clean_output,
        "latency": latency
    }