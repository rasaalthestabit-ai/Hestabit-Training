import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

API_BASE = "http://localhost:8000"
GROQ_KEY = os.getenv("GROQ_API_KEY")

st.set_page_config(page_title="NEXUS AI", page_icon="◈")

st.title("◈ NEXUS AI")

# ─────────────────────────────────────────────
# Session state
# ─────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = None

# ─────────────────────────────────────────────
# Display chat history
# ─────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ─────────────────────────────────────────────
# Chat input
# ─────────────────────────────────────────────
prompt = st.chat_input("Enter your goal…")

if prompt:
    if not GROQ_KEY:
        st.error("Missing GROQ_API_KEY in .env")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    step_labels = {
        1: "🔍 Orchestrator — analysing goal",
        2: "📋 Planner — decomposing into sub-tasks",
        3: "⚙️  DAG Executor — running agents",
        4: "🔎 Critic — reviewing outputs",
        5: "✨ Optimizer — improving outputs",
        6: "✅ Validator — certifying result",
        7: "📄 Reporter — compiling final report",
    }

    reply = ""

    with st.chat_message("assistant"):
        progress   = st.empty()
        result_box = st.empty()

        try:
            with requests.post(
                f"{API_BASE}/run/stream",
                json={
                    "goal":       prompt,
                    "data":       "",
                    "session_id": st.session_state.session_id,
                    "api_key":    GROQ_KEY,
                },
                stream=True,
                timeout=300,
            ) as resp:

                collected_report = ""
                validation_info  = {}

                for raw_line in resp.iter_lines():
                    if not raw_line:
                        continue
                    line = raw_line.decode("utf-8") if isinstance(raw_line, bytes) else raw_line
                    if not line.startswith("data:"):
                        continue

                    payload = json.loads(line[5:].strip())
                    event   = payload.get("event")
                    data    = payload.get("data", {})

                    if event == "start":
                        st.session_state.session_id = data.get("session_id", "")
                        progress.info(f"🚀 Session `{st.session_state.session_id}`")

                    elif event == "step":
                        step_n = data.get("step", "?")
                        status = data.get("status", "")
                        label  = step_labels.get(step_n, f"Step {step_n}")
                        if status == "running":
                            progress.info(f"⏳ {label}…")
                        elif status == "done":
                            progress.success(f"{label} — done")

                    elif event == "node":
                        name   = data.get("name", "")
                        agent  = data.get("agent", "")
                        status = data.get("status", "")
                        if status == "running":
                            progress.info(f"  ▸ [{agent.upper()}] {name}…")
                        elif status == "done":
                            progress.success(f"  ✅ [{agent.upper()}] {name}")
                        elif status == "failed":
                            progress.warning(f"  ❌ [{agent.upper()}] {name} — {data.get('error', '')}")

                    elif event == "complete":
                        validation_info  = data.get("validation", {})
                        collected_report = data.get("final_report", "")
                        st.session_state.session_id = data.get("session_id", st.session_state.session_id)
                        progress.empty()

                    elif event == "error":
                        progress.error(f"Pipeline error: {data.get('message')}")

            if collected_report:
                verdict = validation_info.get("verdict", "?")
                score   = validation_info.get("score", "?")
                reply   = (
                    f"**Verdict:** `{verdict}`  •  **Score:** `{score}/10`\n\n"
                    "---\n\n"
                    + collected_report
                )
            else:
                reply = "Pipeline completed — check `outputs/reports/` for the full report."

            result_box.markdown(reply)

        except Exception as e:
            reply = f"❌ Error: {e}"
            result_box.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})