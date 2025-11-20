import sqlite3

DB_NAME = "expenses.db"


def get_db_connection():
    """
    Create and return a SQLite database connection.

    The connection uses the global DB_NAME and enables row access
    by column name through sqlite3.Row as the row factory.
    """
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """
    Initialize the database schema.

    Creates the 'expenses' table if it does not already exist.
    The table stores basic expense information including title,
    numeric amount, optional category, and a date string.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT,
            date TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()
