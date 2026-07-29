from app.llm import ask_llm
from app.schema import get_schema


def clean_sql(response: str) -> str:
    response = response.strip()

    # Remove Markdown code fences
    if response.startswith("```"):
        lines = response.splitlines()

        # Remove opening ``` or ```sql
        lines = lines[1:]

        # Remove closing ```
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        response = "\n".join(lines)

    # Remove a leading 'sql' if present
    if response.lower().startswith("sql"):
        response = response[3:]

    return response.strip()


def generate_sql(question: str) -> str:
    schema = get_schema()

    prompt = (
        f"You are a SQLite expert. Database schema:\n{schema}\n\n"
        f"Write ONE SQLite query for this question. "
        f"Return ONLY the SQL, no explanation, no markdown.\n"
        f"Question: {question}"
    )

    sql = ask_llm(prompt)

    return clean_sql(sql)