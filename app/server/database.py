import sqlite3
import os
from cryptography.fernet import Fernet
import bcrypt
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# bcrypt Config
BCRYPT_ROUNDS = 12

# Fernet Config
FERNET_KEY = os.getenv('FERNET_KEY')
if not FERNET_KEY:
    raise RuntimeError("FERNET_KEY not set in environment (.env)")
fernet = Fernet(FERNET_KEY.encode())

con = sqlite3.connect("noticeboard.db")

# Init database
def init_database():
    cur = con.cursor()
    
    # Users
    cur.execute("""
        CREATE TABLE IF NOT EXISTS
             users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            )
    """)

    cur.execute("DELETE FROM users")
    cur.execute("DELETE FROM SQLITE_SEQUENCE WHERE name='users'")

    admin_phone_enc = fernet.encrypt(b'+3530839990000').decode()
    admin_pass_hash = bcrypt.hashpw(b'admin1234', bcrypt.gensalt(BCRYPT_ROUNDS)).decode()
    cur.execute("INSERT INTO users VALUES (NULL, ?, ?, ?, ?, ?)",
                ('Admin', admin_phone_enc, 'admin', admin_pass_hash, 'administrator'))

    # Messages
    cur.execute("""
        CREATE TABLE IF NOT EXISTS
             messages (
                message_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                message TEXT NOT NULL,
                date TEXT NOT NULL,
                user_id INTEGER NOT NULL
            )
    """)

    cur.execute("DELETE FROM messages")
    cur.execute("DELETE FROM SQLITE_SEQUENCE WHERE name='messages'")

    con.commit()

# Queries

def insert(query, params):
    try:
        cur = con.cursor()
        res = cur.execute(query, params)
        con.commit()
        return res.lastrowid
    except Exception as error:
        print(error)
        return None

def selectOne(query, params):
    try:
        cur = con.cursor()
        res = cur.execute(query, params)
        row = res.fetchone()
        return row
    except Exception as error:
        print(error)
        return None

def selectAll(query, params):
    try:
        cur = con.cursor()
        res = cur.execute(query, params)
        rows = res.fetchall()
        return rows
    except Exception as error:
        print(error)
        return []

# Auth
def add_user(name, phone, username, password):
    phone_enc = fernet.encrypt(phone.encode()).decode()
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt(BCRYPT_ROUNDS)).decode()

    query = f"INSERT INTO users VALUES (NULL, ?, ?, ?, ?, 'user')"
    params = (name, phone_enc, username, password_hash)
    id = insert(query, params)
    return id
    
def login(username, password):
    query = f"SELECT * FROM users WHERE username = ?"
    params = (username,)
    user = selectOne(query, params)

    if not user:
        return None

    user_password_hash = user[4]

    if not bcrypt.checkpw(password.encode(), user_password_hash.encode()):
        return None

    return user

# Messages
def get_messages():
    query = f"SELECT * FROM messages LEFT OUTER JOIN users USING(user_id) ORDER BY date DESC"
    params = ()
    messages = selectAll(query, params)
    return messages

def add_message(title, message, user_id):
    query = f"INSERT INTO messages VALUES (NULL, ?, ?, datetime('now'), ?)"
    params = (title, message, user_id)
    id = insert(query, params)
    return id

