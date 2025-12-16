import sqlite3

con = sqlite3.connect("noticeboard.db")

# ' OR 1<>2 /* '

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

    cur.execute("INSERT INTO users VALUES (NULL, 'Admin', '+3530839990000', 'admin', 'admin1234', 'administrator')")

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


# Queries

def insert(query, params):
    try:
        cur = con.cursor()
        res = cur.execute(query, params)
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
    query = f"INSERT INTO users VALUES (NULL, ?, ?, ?, ?, 'user')"
    params = (name, phone, username, password)
    id = insert(query, params)
    return id
    
def login(username, password):
    query = f"SELECT * FROM users WHERE username = ? AND password = ?"
    params = (username, password)
    user = selectOne(query, params)
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

