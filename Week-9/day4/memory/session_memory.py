import sqlite3
import requests

DB_PATH = "memory/long_term.db"

class SessionMemory:
    def __init__(self, user_id, max_messages=10):
        self.messages = []
        self.max_messages = max_messages
        self.user_id = user_id
        self._init_db()

    def _init_db(self):
        """Initialize SQLite long-term memory database"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS long_term_memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                fact TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()
        print("Long-term memory database initialized!")

    def add_message(self, role, content):
        """Add message to session memory"""
        self.messages.append({
            "role": role,
            "content": content
        })
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]

    def get_context(self):
        """Get conversation as a single string"""
        context = ""
        for msg in self.messages:
            context += f"{msg['role']}: {msg['content']}\n"
        return context

    def summarize_facts(self):
        """Use Mistral to summarize important facts from conversation"""
        if not self.messages:
            print("No messages to summarize!")
            return None

        conversation = self.get_context()

        prompt = f"""
        Extract only the important facts about the user from this conversation.
        Return a short bullet point list of facts only.
        No extra explanation.

        Conversation:
        {conversation}

        Important facts:
        """

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False
            }
        )

        facts = response.json()["response"].strip()
        print(f"Summarized facts:\n{facts}")
        return facts

    def save_facts_to_db(self, facts):
        """Save summarized facts to SQLite long-term memory"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO long_term_memory (user_id, fact) VALUES (?, ?)",
            (self.user_id, facts)
        )
        conn.commit()
        conn.close()
        print(f"Facts saved for user: {self.user_id}")

    def get_long_term_facts(self):
        """Retrieve facts for this specific user"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT fact, created_at FROM long_term_memory WHERE user_id = ? ORDER BY created_at DESC",
            (self.user_id,)
        )
        rows = cursor.fetchall()
        conn.close()
        return rows

    def clear_session(self):
        """Clear session memory"""
        self.messages = []
        print("Session memory cleared!")