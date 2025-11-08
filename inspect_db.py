import sqlite3

conn = sqlite3.connect("cultivar.db")
cursor = conn.cursor()
try:
    cursor.execute("SELECT * FROM alembic_version")
    print(cursor.fetchall())
except sqlite3.OperationalError:
    print("alembic_version table not found.")
finally:
    conn.close()
