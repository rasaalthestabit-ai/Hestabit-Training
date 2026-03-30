import os
import sqlite3
from generator.sql_generator import SQLGenerator
from utils.schema_loader import SchemaLoader


class SQLPipeline:
    def __init__(self, db_path):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        if db_path is None:
            self.db_path = os.path.join(BASE_DIR, "data", "raw", "db.sqlite")
        else:
            self.db_path = db_path

        print("CURRENT WORKING DIR:", os.getcwd())
        print("DB PATH:", db_path)
        print("EXISTS:", os.path.exists(db_path))

        self.generator = SQLGenerator()
        self.schema_loader = SchemaLoader(db_path)

    # -------------------------------
    # VALIDATOR (basic safety)
    # -------------------------------
    def validate_query(self, query):
        forbidden = ["DROP", "DELETE", "INSERT", "UPDATE", "ALTER"]

        for word in forbidden:
            if word in query.upper():
                raise ValueError(f"❌ Unsafe query detected: {word}")

        return True

    # -------------------------------
    # EXECUTOR
    # -------------------------------
    def execute_query(self, query):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(query)
        results = cursor.fetchall()

        conn.close()
        return results

    # -------------------------------
    # MAIN PIPELINE
    # -------------------------------
    def run(self, question):
        print("\n🔍 Loading schema...")
        schema = self.schema_loader.load_schema()

        print("\n🧠 Generating SQL...")
        sql_query = self.generator.generate_sql(question, schema)
        print(f"\n📝 Generated SQL:\n{sql_query}")

        print("\n🛡️ Validating query...")
        self.validate_query(sql_query)

        print("\n⚙️ Executing query...")
        results = self.execute_query(sql_query)
        print(f"\n📊 Raw Results:\n{results}")

        print("\n🤖 Summarizing...")
        answer = self.generator.summarize(question, results)

        print("\n✅ Final Answer:")
        print(answer)


# -------------------------------
# RUN
# -------------------------------
if __name__ == "__main__":
    db_path = "src/data/raw/db.sqlite"   # change if needed

    pipeline = SQLPipeline(db_path)

    while True:
        q = input("\n❓ Ask SQL question (or 'exit'): ")

        if q.lower() == "exit":
            break

        try:
            pipeline.run(q)
        except Exception as e:
            print(f"\n❌ Error: {e}")