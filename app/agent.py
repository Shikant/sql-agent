import sqlglot
from app.llm import ask_llm
from app.schema import get_schema
from app.schema_notes import NOTES


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

def is_valid(sql: str) -> bool:
    try:
        sqlglot.parse_one(sql, read="sqlite")
        return True
    except Exception:
        return False


def generate_sql(question: str) -> str:
    schema = get_schema()

    notes = "\n".join(
    f"{table}: {description}"
    for table, description in NOTES.items()
    )

    prompt = (
    f"You are a SQLite expert.\n\n"
    f"Database schema:\n"
    f"{schema}\n\n"
    f"Table notes:\n"
    f"{notes}\n\n"
    f"Write ONE SQLite query for this question.\n"
    f"Return ONLY the SQL, no explanation, no markdown.\n\n"
    f"Question: {question}"
    )

    sql = ask_llm(prompt)

    return clean_sql(sql)

def generate_and_run(question, max_tries=3):
    from app.db import run_sql
    error = None; sql = ''
    for attempt in range(max_tries):
        hint = f'\nThe previous query failed with this error: {error}. Fix it.' if error else ''
        sql = generate_sql(question + hint)
        result = run_sql(sql)
        if result['ok']:
            return {'sql': sql, 'rows': result['rows'], 'tries': attempt+1}
        error = result['error']
    return {'sql': sql, 'rows': [], 'error': error, 'tries': max_tries}