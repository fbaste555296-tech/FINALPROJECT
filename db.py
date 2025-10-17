import sqlite3

DB_FILE = "clinic_final.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            doctor TEXT,
            date TEXT,
            time TEXT,
            status TEXT DEFAULT 'Booked',
            payment TEXT DEFAULT 'Unpaid'
        )
    """)
    cur.execute("SELECT id FROM users WHERE role='Admin' LIMIT 1")
    if not cur.fetchone():
        cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                    ("admin", "admin123", "Admin"))
    conn.commit()
    conn.close()
