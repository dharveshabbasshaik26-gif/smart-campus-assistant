import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# ---------------- CREATE ADMIN ----------------
password = generate_password_hash("admin123")

cursor.execute(
"""
INSERT OR IGNORE INTO users(username,password_hash,role)
VALUES (?,?,?)
""",
("admin", password, "admin")
)

# ---------------- SAMPLE COURSES ----------------
cursor.execute("""
INSERT OR IGNORE INTO courses(course,fees,duration,eligibility)
VALUES('B.Tech','120000','4 years','Intermediate')
""")

cursor.execute("""
INSERT OR IGNORE INTO courses(course,fees,duration,eligibility)
VALUES('MCA','80000','2 years','Bachelor Degree')
""")

cursor.execute("""
INSERT OR IGNORE INTO courses(course,fees,duration,eligibility)
VALUES('MBA','90000','2 years','Bachelor Degree')
""")

conn.commit()
conn.close()

print("Admin user and sample courses created")