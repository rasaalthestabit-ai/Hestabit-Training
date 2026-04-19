from orchestrator.planner import Planner

if __name__ == "__main__":
    planner = Planner()

    query = input("Enter your query: ")

    result = planner.execute(query)

    print("\nFinal Answer:\n", result)