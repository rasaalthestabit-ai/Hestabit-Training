# AGENT-FUNDAMENTALS.md
## Day 1 — Agent Foundations + Message-Based Communication

---

## 1. What is an AI Agent?

An **AI agent** is a system that perceives its environment, reasons about it, and takes actions to achieve a goal — in a loop, autonomously.

```
Perception → Reasoning → Action → (repeat)
```

| Component   | In this project                                      |
|-------------|------------------------------------------------------|
| Perception  | Receives a message (string) as input                 |
| Reasoning   | LLM processes the message using its system prompt    |
| Action      | Produces a message passed to the next agent          |

---

## 2. Agent vs Chatbot vs Pipeline

| Concept   | Description                                                                 |
|-----------|-----------------------------------------------------------------------------|
| Chatbot   | Single LLM, single turn or simple memory, no goal-directed behavior         |
| Pipeline  | Fixed sequence of deterministic steps, no reasoning between steps           |
| **Agent** | Goal-directed, reasons before acting, can have memory, tools, and sub-goals |

This project is a **multi-agent pipeline** — each agent has a distinct role and communicates via messages.

---

## 3. Perception → Reasoning → Action Loop

```
User Query
    │
    ▼
┌─────────────────────┐
│   Research Agent    │  Perception: receives user query
│   (ReAct loop)      │  Reasoning:  Thought → Action → Observation
│                     │  Action:     emits research notes
└────────┬────────────┘
         │ research notes
         ▼
┌─────────────────────┐
│  Summarizer Agent   │  Perception: receives research notes
│   (ReAct loop)      │  Reasoning:  identify key points
│                     │  Action:     emits bullet-point summary
└────────┬────────────┘
         │ summary
         ▼
┌─────────────────────┐
│   Answer Agent      │  Perception: receives summary
│   (ReAct loop)      │  Reasoning:  compose user-facing answer
│                     │  Action:     emits final answer
└────────┬────────────┘
         │ final answer
         ▼
      User
```

---

## 4. The ReAct Pattern (Reason + Act)

**ReAct** = **Re**asoning + **Act**ing interleaved in the prompt.

Each agent's system prompt enforces this format:

```
Thought:     What do I need to do?
Action:      What step am I taking?
Observation: What did I find / produce?
... (repeat until done)
Final Output: <result>
[TAG_DONE]
```

**Why it works:** Forces the LLM to reason explicitly before producing output, reducing hallucination and improving traceability.

---

## 5. LLM as a Tool Executor

In AutoGen, the LLM is not just a chatbot — it is the **execution engine** of an agent. Each `ConversableAgent`:

- Holds a `system_message` defining its role and constraints.
- Processes incoming messages through the LLM.
- Returns a structured response that drives the next step.

No external tool calls are needed for Day 1. The LLM itself *is* the tool.

---

## 6. System Prompts for Agents

Each agent has a **unique, constrained system prompt** that enforces role isolation:

| Agent      | System Prompt Goal                             | Terminal Tag        |
|------------|------------------------------------------------|---------------------|
| Research   | Gather raw information, no summarizing         | `[RESEARCH_DONE]`   |
| Summarizer | Compress notes to bullets, no new info         | `[SUMMARY_DONE]`    |
| Answer     | Write final answer from summary, no re-research| `[ANSWER_DONE]`     |

**Role isolation** is enforced by the system prompt: each agent is explicitly told what it must NOT do, preventing role bleed.

---

## 7. Message Protocol

Agents communicate by passing plain text messages. The output of each agent is the input of the next:

```python
research_output  → summarizer_agent.initiate_chat(message=research_output)
summarizer_output → answer_agent.initiate_chat(message=summarizer_output)
```

This is **message-based communication**: agents are decoupled and only share data through the message string.

---

## 8. Memory Window

Each agent is configured with:

```python
max_consecutive_auto_reply=10   # memory window = 10 turns
```

This means each agent retains up to 10 turns of conversation history in its context window. For single-turn pipelines this is a safety cap; for multi-turn agents it acts as a rolling memory.

---

## 9. Tech Stack

| Component         | Tool / Library                          |
|-------------------|-----------------------------------------|
| Agent Framework   | AutoGen (Microsoft) — `pyautogen`       |
| LLM               | Mistral / TinyLlama / Phi-3 / Qwen via Ollama |
| LLM API           | Ollama OpenAI-compatible endpoint       |
| Vector Memory     | FAISS (ready to integrate in Day 2+)    |
| API Server        | FastAPI (ready to wrap in Day 2+)       |
| Storage           | SQLite (ready for persistence in Day 2+)|
| Containerization  | Docker (optional, see below)            |

---

## 10. Project Structure

```
agents/
├── research_agent.py      # Research Agent definition
├── summarizer_agent.py    # Summarizer Agent definition
├── answer_agent.py        # Answer Agent definition
├── main.py                # Pipeline orchestrator
└── AGENT-FUNDAMENTALS.md  # This file
```

---

## 11. Setup & Run

### Prerequisites

```bash
# 1. Install Ollama and pull a model
curl -fsSL https://ollama.com/install.sh | sh
ollama pull mistral          # or: tinyllama / phi3 / qwen2

# 2. Install Python dependencies
pip install pyautogen        # AutoGen framework
# pip install faiss-cpu      # for Day 2 memory integration
# pip install fastapi uvicorn # for Day 2 API server
# pip install sqlite3        # stdlib, no install needed
```

### Run the pipeline

```bash
cd agents/
python main.py
```

### Test individual agents

```bash
python research_agent.py    # interactive research test
python summarizer_agent.py  # paste notes, get summary
python answer_agent.py      # paste summary, get answer
```

### Docker (optional)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY agents/ .
RUN pip install pyautogen
# Ollama must be accessible at host.docker.internal:11434
ENV OLLAMA_HOST=http://host.docker.internal:11434
CMD ["python", "main.py"]
```

```bash
docker build -t day1-agents .
docker run -it --add-host host.docker.internal:host-gateway day1-agents
```

---

## 12. Key Concepts Checklist

- [x] What is an AI agent?
- [x] Agent vs chatbot vs pipeline
- [x] Perception → Reasoning → Action loop
- [x] Message protocol / message-based communication
- [x] Agent architecture (role, system prompt, memory, LLM config)
- [x] ReAct pattern (Reason + Act)
- [x] LLM as a tool executor
- [x] System prompts for agents
- [x] Role isolation (strict job separation)
- [x] Memory window (max_consecutive_auto_reply = 10)