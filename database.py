import sqlite3
import json
import os
from flask import g
from config import DB_PATH
from utils.logger import setup_logger

logger = setup_logger(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB_PATH)
        db.row_factory = sqlite3.Row
    return db

def close_db(e=None):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    if not os.path.exists(DB_PATH):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    phone TEXT PRIMARY KEY,
                    state TEXT NOT NULL,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            conn.close()
            logger.info("Database initialized successfully.")
        except Exception as e:
            logger.critical(f"Failed to initialize database: {e}")

def chat_connection():
    """Independent connection helper."""
    return sqlite3.connect(DB_PATH)

def get_user_state(phone: str) -> dict:
    """Retrieves user state from DB as a dictionary."""
    conn = chat_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT state FROM users WHERE phone = ?", (phone,))
        row = cursor.fetchone()
        if row:
            return json.loads(row[0])
        return {} # Empty state if new user
    except sqlite3.Error as e:
        logger.error(f"DB Error getting state for {phone}: {e}")
        return {}
    finally:
        conn.close()

def save_user_state(phone: str, state: dict):
    """Saves user state dictionary to DB."""
    conn = chat_connection()
    try:
        cursor = conn.cursor()
        state_json = json.dumps(state)
        # Upsert logic
        cursor.execute('''
            INSERT INTO users (phone, state) VALUES (?, ?)
            ON CONFLICT(phone) DO UPDATE SET state=excluded.state, updated_at=CURRENT_TIMESTAMP
        ''', (phone, state_json))
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"DB Error saving state for {phone}: {e}")
    finally:
        conn.close()

def reset_user_state(phone: str):
    """Resets user state to empty/initial."""
    save_user_state(phone, {})
