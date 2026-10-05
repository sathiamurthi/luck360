import sqlite3
conn = sqlite3.connect('lottery.db')
for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'"):
    print(row[0])
    for col in conn.execute(f"PRAGMA table_info({row[0]})"):
        print('  ', col)
