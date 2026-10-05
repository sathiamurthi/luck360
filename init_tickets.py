import sqlite3

def init_tickets():
    conn = sqlite3.connect('lottery.db')
    conn.execute('''
    CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY,
        date TEXT,
        slot INTEGER,
        result TEXT,
        cost INTEGER,
        win INTEGER,
        net INTEGER,
        text TEXT,
        rates TEXT,
        repeats BOOLEAN,
        breakdown TEXT
    )
    ''')
    conn.commit()
    conn.close()

init_tickets()
