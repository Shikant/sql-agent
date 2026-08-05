import sqlite3

def get_conn():
    return sqlite3.connect('chinook.db')

def run_sql(sql: str):
    try:
        con = sqlite3.connect('chinook.db')
        return {
            'ok': True,
            'rows': [list(r) for r in con.execute(sql).fetchall()]
        }
    except Exception as e:
        return {
            'ok': False,
            'error': str(e)
        }

if __name__ == '__main__':
    rows = get_conn().execute('SELECT Name FROM Artist LIMIT 5').fetchall()
    print(rows)

