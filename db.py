import sqlite3
from datetime import datetime

DB_FILE = "chatbot.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    #user table
    c.execute("""
              CREATE TABLE IF NOT EXISTS users (
              id INTEGER PRIMARY KEY AUTOINCREMENT , username TEXT UNIQUE NOT NULL)
              """)
    
    # history table 

    c.execute(
       """
         CREATE TABLE IF NOT EXISTS messages (
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         user_id INTEGER,
         role TEXT,
         content TEXT,
         timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
         FOREIGN KEY (user_id) REFERENCES users(id))

        """


       )
    conn.commit()
    conn.close()


def get_or_create_user(username):
    if not username:  # Vérifiez si le username est valide
        raise ValueError("Username cannot be empty")
    
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE username = ?", (username,))
    row = c.fetchone()
    if row:
        user_id = row[0]
    else:
        c.execute("INSERT INTO users (username) VALUES (?)", (username,))
        conn.commit()
        user_id = c.lastrowid
    conn.close()
    return user_id

def save_message(user_id, role, content):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute(
        "INSERT INTO messages (user_id, role, content) VALUES (?,?,?)",
        (user_id, role, content,)
    )
    conn.commit()
    conn.close()

def get_history(user_id):
    
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        "SELECT role, content FROM messages WHERE user_id =? ORDER BY timestamp",
        (user_id,)
    )
    rows = c.fetchall()
    conn.close()
    return [{"role" : role, "content" : content} for role, content in rows]
        
    
    
