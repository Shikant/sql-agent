import sqlite3

def get_conn():
    return sqlite3.connect('chinook.db')

def run_sql(sql: str):
    con = sqlite3.connect('chinook.db')
    cur = con.execute(sql)
    return [list(r) for r in cur.fetchall()]

if __name__ == '__main__':
    rows = get_conn().execute('SELECT Name FROM Artist LIMIT 5').fetchall()
    print(rows)

