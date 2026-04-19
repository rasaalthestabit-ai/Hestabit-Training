import requests
import json
import sys
sys.path.append('./memory')

from memory.session_memory import SessionMemory
from memory.vector_store import VectorStore


# =========================
# LLM GENERATION FUNCTION
# =========================
def generate_with_context(query, context):
    prompt = f"""You are a helpful assistant.

Context:
{context}

User: {query}
Assistant:
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2",
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        data = response.json()

        print("RAW LLM RESPONSE:", data)

        if "response" in data:
            return data["response"].strip()

        if "error" in data:
            return f"LLM Error: {data['error']}"

        return "LLM returned unexpected format"

    except requests.exceptions.Timeout:
        return "Request failed: Timeout from LLM"

    except Exception as e:
        return f"Request failed: {str(e)}"


# =========================
# PIPELINE
# =========================
def run_pipeline(user_query, session, vector_store):

    print(f"\nUser: {user_query}")
    print("-" * 40)

    # STEP 1: MEMORY SEARCH
    print("Step 1: Searching memory...")
    faiss_context = vector_store.get_context_for_query(user_query)
    session_context = session.get_context()

    # Combine contexts
    context = ""
    if session_context:
        context += f"Current conversation:\n{session_context}\n"
    if faiss_context:
        context += f"{faiss_context}"

    # LIMIT CONTEXT SIZE (IMPORTANT FIX)
    context = "\n".join(context.split("\n")[-8:])

    # STEP 2: SHOW CONTEXT
    if context.strip():
        print(f"Step 2: Found relevant context:\n{context}")
    else:
        print("Step 2: No relevant context found")

    # STEP 3: GENERATE RESPONSE
    print("Step 3: Generating response...")
    response = generate_with_context(user_query, context)

    # STEP 4: STORE IN SESSION MEMORY
    session.add_message("user", user_query)

    # Only store valid responses
    if "Request failed" not in response and "Error" not in response:
        session.add_message("assistant", response)

        # Store compact memory (important fix)
        vector_store.add_text(f"User: {user_query} | Assistant: {response}")

    else:
        print("Skipping memory storage due to failed LLM response")

    print(f"Assistant: {response}")
    return response


# =========================
# MAIN LOOP
# =========================
if __name__ == "__main__":

    print("=" * 60)
    print("Agent Memory System - Day 4")
    print("=" * 60)

    username = input("Enter your name: ").strip()
    print(f"\nWelcome {username}!")

    session = SessionMemory(user_id=username, max_messages=10)
    vector_store = VectorStore()

    print(f"\nLoading memory for {username}...")
    vector_store.load_from_db(user_id=username)

    print("\nStarting conversation... (type 'quit' to exit)")
    print("=" * 60)

    while True:
        user_input = input("\nYou: ").strip()

        if not user_input:
            continue

        if user_input.lower() == "quit":
            print("\nSummarizing and saving facts...")

            facts = session.summarize_facts()
            if facts:
                session.save_facts_to_db(facts)
                vector_store.add_text(facts)
                print("Facts saved to long-term memory!")

            print(f"Goodbye {username}!")
            break

        run_pipeline(user_input, session, vector_store)