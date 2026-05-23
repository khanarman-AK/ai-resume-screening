import sqlite3
import os

# Create database inside temp folder

db_path = os.path.join(os.environ["TEMP"], "database.db")

conn = sqlite3.connect(db_path)

cursor = conn.cursor()

cursor.execute("""

CREATE TABLE IF NOT EXISTS resumes (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    candidate_name TEXT,

    score REAL,

    skills TEXT,

    job_description TEXT

)

""")

conn.commit()

conn.close()

print("Database created successfully at:")
print(db_path)