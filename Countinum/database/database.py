import sqlite3
import os

def get_connection():
    # ✅ FIX 2: Create the data/ directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect("data/empire.db")
    conn.row_factory = sqlite3.Row
    return conn
