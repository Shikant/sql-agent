import sqlite3
def get_schema():
    con = sqlite3.connect('chinook.db')
    tables = con.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    out = []
    for (t,) in tables:
        cols = con.execute(f'PRAGMA table_info({t})').fetchall()
        out.append(f"{t}(" + ', '.join(c[1] for c in cols) + ')')
    return '\n'.join(out)
if __name__ == '__main__':
    print(get_schema())