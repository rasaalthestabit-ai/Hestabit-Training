from concurrent.futures import ThreadPoolExecutor
from agents.worker_agent import WorkerAgent
from agents.validator import Validator


class Planner:
    def __init__(self):
        self.worker = WorkerAgent()
        self.validator = Validator()

    def plan(self, query: str):
        return [
            f"Define: {query}",
            f"Give key facts: {query}"
        ]

    def refine(self, outputs: list) -> str:
        # Minimal merge (no extra LLM → faster + safer)
        return " ".join(outputs)

    def execute(self, query: str):
        tasks = self.plan(query)

        # Execution Tree (simple)
        tree = {
            "User Query": query,
            "Tasks": tasks,
            "Workers": [],
            "Final": None
        }

        # Parallel workers
        with ThreadPoolExecutor() as executor:
            results = list(executor.map(self.worker.run, tasks))

        tree["Workers"] = results

        # Internal refinement
        refined = self.refine(results)

        # Validation
        final = self.validator.run(refined)

        tree["Final"] = final

        return final