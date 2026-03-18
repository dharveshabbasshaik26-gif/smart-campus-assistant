import sqlite3

# connect to database (it will be created if not exists)
conn = sqlite3.connect("database.db")

cursor = conn.cursor()


# ---------------- USERS (ADMIN) ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT UNIQUE NOT NULL,
password_hash TEXT NOT NULL,
role TEXT NOT NULL
)
""")


# ---------------- STUDENTS ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT UNIQUE NOT NULL,
password_hash TEXT NOT NULL,
name TEXT,
email TEXT
)
""")


# ---------------- COURSES ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS courses (
id INTEGER PRIMARY KEY AUTOINCREMENT,
course TEXT NOT NULL,
fees TEXT,
duration TEXT,
eligibility TEXT
)
""")


# ---------------- SPECIALISATIONS ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS specialisations (
id INTEGER PRIMARY KEY AUTOINCREMENT,
course_id INTEGER,
specialisation TEXT,
FOREIGN KEY(course_id) REFERENCES courses(id)
)
""")


# ---------------- FACILITIES ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS facilities (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
fees TEXT,
duration TEXT
)
""")


# ---------------- KNOWLEDGE BASE ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS knowledge_base (
id INTEGER PRIMARY KEY AUTOINCREMENT,
question TEXT,
answer TEXT
)
""")


# ---------------- CHATBOT LOGS ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS logs (
id INTEGER PRIMARY KEY AUTOINCREMENT,
message TEXT,
detected_lang TEXT,
translated_message TEXT,
created_at TEXT
)
""")


conn.commit()
conn.close()

print("✅ Database and tables created successfully!")