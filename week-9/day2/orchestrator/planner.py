import json
import re
from agents.worker_agent import WorkerAgent
from agents.validator import ValidatorAgent
from config import call_llm


def fallback_tasks(query: str) -> list:
    return [
        {"id": "t1", "description": f"Gather information about: {query}", "depends_on": []},
        {"id": "t2", "description": f"Analyze key points of: {query}", "depends_on": []},
        {"id": "t3", "description": f"Write a complete answer about: {query}", "depends_on": ["t1", "t2"]},
    ]


def extract_json_array(text: str):
    text = text.strip()

    text = text.replace("```json", "").replace("```", "")

    try:
        return json.loads(text)
    except:
        pass

    match = re.search(r'\[\s*{.*}\s*\]', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except:
            pass

    return None


def generate_task_graph(query: str) -> list:
    prompt = (
    f"You are an expert planner agent.\n\n"

    f"STEP 1: Identify all distinct questions or topics in the query.\n"
    f"STEP 2: Break them into atomic tasks (one concept per task).\n"
    f"STEP 3: Create additional tasks ONLY if needed for synthesis or relationships.\n\n"

    f"IMPORTANT RULES:\n"
    f"- Each task must focus on ONE concept only\n"
    f"- DO NOT merge unrelated concepts into one task\n"
    f"- Create separate tasks for each question\n"
    f"- Only use 'depends_on' if a task truly requires previous outputs\n"
    f"- Tasks without dependencies will run in parallel\n"
    f"- Total tasks should be between 3 and 6\n"
    f"- Output MUST be valid JSON\n"
    f"- No explanations, no markdown, no extra text\n\n"

    f"Query:\n{query}\n\n"

    f"Output format:\n"
    f'[\n'
    f'  {{"id":"t1","description":"...","depends_on":[]}},\n'
    f'  {{"id":"t2","description":"...","depends_on":[]}},\n'
    f'  {{"id":"t3","description":"...","depends_on":[]}},\n'
    f'  {{"id":"t4","description":"...","depends_on":["t1","t3"]}}\n'
    f']'
)

    raw = call_llm(prompt, max_tokens=300)

    tasks = extract_json_array(raw)

    if not tasks:
        print("  [Planner] JSON parse failed, using fallback task graph.")
        return fallback_tasks(query)

    try:
        for t in tasks:
            assert "id" in t and "description" in t and "depends_on" in t
        return tasks
    except Exception:
        print("  [Planner] Invalid structure, using fallback task graph.")
        return fallback_tasks(query)


def build_waves(tasks: list) -> list:
    completed = set()
    remaining = {t["id"]: t for t in tasks}
    waves = []

    while remaining:
        wave = [
            tid for tid, t in remaining.items()
            if all(dep in completed for dep in t.get("depends_on", []))
        ]
        if not wave:
            wave = list(remaining.keys())
        waves.append(wave)
        for tid in wave:
            completed.add(tid)
            del remaining[tid]

    return waves


def reflect(query: str, tasks: list, results: dict) -> str:
    task_outputs = "\n".join(
        f"- {t['id']}: {results.get(t['id'], '')}" for t in tasks
    )
    prompt = (
        f"Synthesize these task results into one clear answer for the query.\n\n"
        f"Query: {query}\n\n"
        f"Task results:\n{task_outputs}\n\n"
        f"Write a coherent final answer:"
    )
    return call_llm(prompt, max_tokens=400)


def run(query: str) -> dict:
    print(f"\n[Planner] Query: {query}")

    print("[Planner] Generating task graph...")
    tasks = generate_task_graph(query)
    task_map = {t["id"]: t for t in tasks}
    print(f"[Planner] {len(tasks)} tasks: {[t['id'] for t in tasks]}")

    waves = build_waves(tasks)
    results = {}
    worker = WorkerAgent()

    print(f"[Planner] Executing {len(waves)} wave(s)...")
    for i, wave in enumerate(waves):
        print(f"[Planner] Wave {i+1}: {wave}")
        for tid in wave:
            results[tid] = worker.execute(task_map[tid], results)

    print("[Planner] Running reflection...")
    reflection = reflect(query, tasks, results)

    print("[Planner] Running validation...")
    validator = ValidatorAgent()
    validation = validator.validate(query, reflection)

    return {
        "query": query,
        "task_graph": tasks,
        "worker_results": results,
        "reflection": reflection,
        "validation_passed": validation["passed"],
        "final_answer": validation["answer"]
    }