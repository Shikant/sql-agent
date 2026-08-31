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


if __name__ == "__main__":
    with get_conn() as con:
        rows = con.execute(
            "SELECT Name FROM Artist LIMIT 5"
        ).fetchall()

    print(rows)