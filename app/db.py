import sqlite3
def get_conn():
    return sqlite3.connect('chinook.db')
if __name__ == '__main__':
    rows = get_conn().execute('SELECT Name FROM Artist LIMIT 5').fetchall()
    print(rows)