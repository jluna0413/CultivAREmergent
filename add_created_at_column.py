import sqlite3

def add_created_at_column():
    db_path = 'data/cultivar.db'  # Path to your SQLite database

    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Add the 'created_at' column to the 'plant' table
        cursor.execute("""
        ALTER TABLE plant ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP;
        """)

        # Commit the changes and close the connection
        conn.commit()
        print("Column 'created_at' added successfully.")
    except sqlite3.OperationalError as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    add_created_at_column()