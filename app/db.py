import sqlite3


def get_conn():
    return sqlite3.connect("chinook.db")


def run_sql(sql: str):
    try:
        with sqlite3.connect("chinook.db") as con:
            rows = con.execute(sql).fetchall()

        return {
            "ok": True,
            "rows": [list(r) for r in rows],
        }

    except Exception as e:
        return {
            "ok": False,
            "error": str(e),
        }


def explain(sql: str):
    with sqlite3.connect("chinook.db") as con:
        return [
            list(r)
            for r in con.execute(
                "EXPLAIN QUERY PLAN " + sql
            ).fetchall()
        ]


def check_query_plan(sql: str):
    plan = explain(sql)
    scanned_tables = []

    for row in plan:
        text = " ".join(str(value) for value in row)

        if "SCAN TABLE" in text:
            scanned_tables.append(text)

    if scanned_tables:
        return "WARNING: Full table scans detected:\n" + "\n".join(scanned_tables)

    return "No full table scans detected."


if __name__ == "__main__":
    sql = "SELECT * FROM Track"

    print(check_query_plan(sql))