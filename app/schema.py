import sqlite3


def get_schema():
    con = sqlite3.connect("chinook.db")
    out = []

    tables = con.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    ).fetchall()

    for (table,) in tables:
        out.append(f"\nTable: {table}")

        # Columns
        cols = con.execute(f"PRAGMA table_info({table})").fetchall()

        out.append("Columns:")
        for col in cols:
            name = col[1]
            col_type = col[2]
            pk = " PRIMARY KEY" if col[5] else ""
            out.append(f"  - {name} ({col_type}){pk}")

        # Foreign keys
        fks = con.execute(f"PRAGMA foreign_key_list({table})").fetchall()
        if fks:
            out.append("Foreign Keys:")
            for fk in fks:
                out.append(
                    f"  - {fk[3]} -> {fk[2]}.{fk[4]}"
                )

        # Example rows
        rows = con.execute(
            f"SELECT * FROM {table} LIMIT 2"
        ).fetchall()

        if rows:
            out.append("Example Rows:")
            for row in rows:
                out.append(f"  {row}")

    con.close()

    return "\n".join(out)


if __name__ == "__main__":
    print(get_schema())