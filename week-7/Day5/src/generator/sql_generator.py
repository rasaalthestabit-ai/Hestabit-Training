import os
from groq import Groq


class SQLGenerator:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "llama-3.1-8b-instant"
    def clean_sql(self, sql):
        # Remove markdown
        sql = sql.replace("```sql", "").replace("```", "")
        
        # Remove extra spaces/newlines
        return sql.strip()

    def generate_sql(self, question, schema):
        prompt = f"""
            You are an expert SQL generator.

            Schema:
            {schema}

            IMPORTANT RULES:
            - Use ONLY SQLite syntax
            - Do NOT use YEAR()
            - Use strftime('%Y', column) for year extraction
            - Return ONLY raw SQL
            - No markdown, no explanation

            Question:
            {question}
            """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
        )

        sql = response.choices[0].message.content.strip()
        return self.clean_sql(sql)

    def summarize(self, question, results):
        prompt = f"""
User Question:
{question}

SQL Results:
{results}

Give a concise human-readable answer.
"""

        response = self.client.chat.completions.create(
    model=self.model,
    messages=[
        {
            "role": "user",
            "content": f"""
You are a helpful assistant.

User question:
{question}

SQL results:
{results}

Summarize the answer in a clear and concise way.
"""
        }
    ],
)

        return response.choices[0].message.content.strip()