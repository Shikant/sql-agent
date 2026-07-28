from app.llm import ask_llm
from app.schema import get_schema
def generate_sql(question: str) -> str:
    schema = get_schema()
    prompt = (f'You are a SQLite expert. Database schema:\n{schema}\n\n'
              f'Write ONE SQLite query for this question. Return ONLY the SQL, no explanation, no markdown.\n'
              f'Question: {question}')
    sql = ask_llm(prompt).strip().strip('`')
    if sql.lower().startswith('sql'): sql = sql[3:].strip()
    return sql