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
        upper_text = text.upper()

        if "SCAN " in upper_text:
            # Index scans are allowed.
            if "USING INDEX" in upper_text:
                continue

            if "USING COVERING INDEX" in upper_text:
                continue

            scanned_tables.append(text)

    if scanned_tables:
        return {
            "ok": False,
            "warning": "Full table scans detected",
            "details": scanned_tables,
            "plan": plan,
        }

    return {
        "ok": True,
        "warning": None,
        "details": [],
        "plan": plan,
    }

if __name__ == "__main__":
    test_queries = {
        "full_scan": "SELECT * FROM Track",
        "primary_key_lookup": (
            "SELECT TrackId, Name "
            "FROM Track "
            "WHERE TrackId = 10"
        ),
        "join_with_filter": """
            SELECT t.Name, a.Title
            FROM Track t
            JOIN Album a ON t.AlbumId = a.AlbumId
            WHERE a.AlbumId = 5
        """,
    }

    for name, sql in test_queries.items():
        print(f"\n--- {name} ---")
        print(f"SQL: {sql.strip()}")

        result = check_query_plan(sql)

        print("Query Plan:")
        for row in result["plan"]:
            print(row)

        if result["ok"]:
            print("No full table scans detected.")
        else:
            print("WARNING: Full table scans detected:")
            for scan in result["details"]:
                print(scan)