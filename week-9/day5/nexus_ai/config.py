import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR    = Path(__file__).parent.parent
NEXUS_DIR   = BASE_DIR / "nexus_ai"
LOGS_DIR    = BASE_DIR / "logs"
OUTPUTS_DIR = BASE_DIR / "outputs"
DATA_DIR    = BASE_DIR / "data"
MEMORY_DIR  = DATA_DIR / "memory"

for d in [LOGS_DIR, OUTPUTS_DIR, DATA_DIR, MEMORY_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# ==============================
# API CONFIG
# ==============================
LLM_PROVIDER   = "groq"
GROQ_API_KEY   = os.getenv("GROQ_API_KEY")
GROQ_BASE_URL  = "https://api.groq.com/openai/v1"

# ==============================
# MODEL STRATEGY
# ==============================
MODELS = {
    "fast":     "llama-3.1-8b-instant", 
    "balanced": "llama-3.3-70b-versatile",    
    "powerful": "llama-3.3-70b-versatile",  
}

# Assign smartly (THIS IS KEY)
DEFAULT_MODEL       = MODELS["fast"]
ORCHESTRATOR_MODEL  = MODELS["balanced"]  
CRITIC_MODEL        = MODELS["balanced"] 
CODER_MODEL         = MODELS["balanced"]

# ==============================
# TOKEN CONTROL (CRITICAL)
# ==============================
MAX_TOKENS          = 800  
TEMPERATURE         = 0.3
REQUEST_TIMEOUT     = 60

# ==============================
# LOOP CONTROL
# ==============================
MAX_ROUNDS                  = 1
MAX_CONSECUTIVE_AUTO_REPLY  = 1 

# ==============================
# MEMORY OPTIMIZATION
# ==============================
EMBEDDING_MODEL       = "sentence-transformers/all-MiniLM-L6-v2"
FAISS_INDEX_PATH      = str(MEMORY_DIR / "faiss.index")
MEMORY_METADATA_PATH  = str(MEMORY_DIR / "metadata.json")
SESSION_LOG_PATH      = str(MEMORY_DIR / "sessions.json")

TOP_K_RECALL          = 2      
MEMORY_THRESHOLD      = 0.75   

# ==============================
# PLANNING CONTROL
# ==============================
MAX_PLAN_DEPTH      = 4         
PLAN_RETRY_LIMIT    = 0

# ==============================
# LOGGING
# ==============================
LOG_LEVEL   = "INFO"
LOG_FILE    = str(LOGS_DIR / "nexus.log")
TRACE_FILE  = str(LOGS_DIR / "trace.jsonl")

# ==============================
# OUTPUT DIRS
# ==============================
CODE_OUTPUT_DIR     = str(OUTPUTS_DIR / "code")
REPORT_OUTPUT_DIR   = str(OUTPUTS_DIR / "reports")
CHART_OUTPUT_DIR    = str(OUTPUTS_DIR / "charts")

for d in [CODE_OUTPUT_DIR, REPORT_OUTPUT_DIR, CHART_OUTPUT_DIR]:
    Path(d).mkdir(parents=True, exist_ok=True)

# ==============================
# AGENTS (UNCHANGED)
# ==============================
AGENT_ROLES = {
    "orchestrator": "Routes tasks, manages agent lifecycle, drives DAG execution.",
    "planner":      "Decomposes goals into ordered sub-tasks; builds execution DAG.",
    "researcher":   "Gathers facts, synthesises knowledge; returns structured findings.",
    "coder":        "Writes, refines, and saves production-quality code.",
    "analyst":      "Processes data, identifies patterns, produces business insights.",
    "critic":       "Reviews outputs for correctness, quality, gaps; scores work.",
    "optimizer":    "Improves prior outputs; applies self-reflection feedback.",
    "validator":    "Runs checks / tests; certifies readiness or flags failures.",
    "reporter":     "Compiles final reports with summaries, findings, and recommendations.",
}