import logging

import sqlglot

from app.db import check_query_plan, run_sql
from app.llm import ask_llm
from app.schema import get_schema
from app.schema_notes import NOTES


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def clean_sql(response: str) -> str:
    response = response.strip()

    if response.startswith("```"):
        lines = response.splitlines()
        lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        response = "\n".join(lines)

    if response.lower().startswith("sql"):
        response = response[3:]

    return response.strip()


def is_valid(sql: str) -> bool:
    try:
        sqlglot.parse_one(sql, read="sqlite")
        return True
    except Exception:
        return False


def generate_sql(
    question: str,
    previous_sql: str = "",
    error: str = "",
) -> str:
    schema = get_schema()

    notes = "\n".join(
        f"{table}: {description}"
        for table, description in NOTES.items()
    )

    retry_context = ""

    if previous_sql and error:
        retry_context = (
            "\n\nThe previous SQL query needs correction.\n"
            f"Previous SQL:\n{previous_sql}\n\n"
            f"Feedback:\n{error}\n\n"
            "Correct the SQL query based on this feedback. "
            "Return ONLY the corrected SQLite SQL."
        )

    prompt = (
        "You are a SQLite expert.\n\n"
        f"Database schema:\n{schema}\n\n"
        f"Table notes:\n{notes}\n\n"
        "Write ONE SQLite query for this question.\n\n"
        "Write efficient SQL:\n"
        "- Use indexed columns in WHERE and JOIN when appropriate.\n"
        "- Never use SELECT *.\n"
        "- Avoid unnecessary full table scans.\n"
        "- Prefer specific columns.\n"
        "- Use primary keys and available indexes when appropriate.\n\n"
        "Return ONLY the SQL, no explanation, no markdown.\n\n"
        f"Question: {question}"
        f"{retry_context}"
    )

    sql = ask_llm(prompt)

    return clean_sql(sql)


def generate_and_run(question: str, max_tries: int = 3):
    previous_sql = ""
    error = ""

    for attempt in range(max_tries):
        logger.info(f"Attempt {attempt + 1}/{max_tries}")

        sql = generate_sql(
            question,
            previous_sql=previous_sql,
            error=error,
        )

        logger.info(f"Generated SQL:\n{sql}")

        # 1. Validate SQL syntax before sending it to SQLite.
        if not is_valid(sql):
            error = "Invalid SQLite syntax"
            previous_sql = sql

            logger.error(f"SQL validation failed: {error}")
            continue

        # 2. Inspect SQLite query plan before executing the query.
        try:
            plan_result = check_query_plan(sql)
        except Exception as e:
            error = f"Could not analyze query plan: {e}"
            previous_sql = sql

            logger.error(error)
            continue

        logger.info(f"Query plan: {plan_result['plan']}")

        # 3. Retry if SQLite reports a full table scan.
        if not plan_result["ok"]:
            error = (
                "The query plan contains a full table scan.\n"
                "Query plan:\n"
                + "\n".join(plan_result["details"])
            )

            previous_sql = sql

            logger.warning(error)
            logger.info(
                "Retrying with query-plan feedback..."
            )
            continue

        # 4. Execute only after SQL validation and query-plan validation.
        result = run_sql(sql)

        if result["ok"]:
            logger.info(
                f"SQL executed successfully on attempt {attempt + 1}"
            )

            return {
                "sql": sql,
                "rows": result["rows"],
                "tries": attempt + 1,
            }

        # 5. Database execution failed. Feed the error back to the LLM.
        error = result["error"]
        previous_sql = sql

        logger.error(f"SQL execution failed: {error}")
        logger.info(
            "Retrying with database error feedback..."
        )

    return {
        "sql": previous_sql,
        "rows": [],
        "error": error,
        "tries": max_tries,
    }