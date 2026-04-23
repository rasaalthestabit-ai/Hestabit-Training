from config import call_llm

class WorkerAgent:
    def execute(self, task: dict, prior_results: dict) -> str:
        task_id = task["id"]
        description = task["description"]
        deps = task.get("depends_on", [])

        context = ""
        if deps:
            context = "\n\nContext from prior tasks:\n" + "\n".join(
                f"- {d}: {prior_results[d]}" for d in deps if d in prior_results
            )

        prompt = f"Complete this task in 2-3 sentences:\nTask: {description}{context}"
        result = call_llm(prompt, max_tokens=200)
        print(f"  [Worker {task_id}] done")
        return result