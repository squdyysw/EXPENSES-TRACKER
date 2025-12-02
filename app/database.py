"""
Database utilities for Expense Tracker.

Provides connection and initialization functions with
logging and error handling.
"""

import sqlite3
from app.logging_info import logger

DB_NAME = "expenses.db"


def get_db_connection():
    """
    Create and return a SQLite database connection.

    The connection uses the global DB_NAME and enables row access
    by column name through sqlite3.Row as the row factory.

    Returns
    -------
    sqlite3.Connection
        SQLite database connection object.
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        logger.info(f"Database connection established to {DB_NAME}")
        return conn
    except sqlite3.Error as e:
        logger.error(f"Error connecting to database {DB_NAME}: {e}")
        raise


def init_db():
    """
    Initialize the database schema.

    Creates the 'expenses' table if it does not already exist.
    The table stores basic expense information including title,
    numeric amount, optional category, and a date string.
    """
    try:
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
        logger.info("Database initialized successfully.")
    except sqlite3.Error as e:
        logger.error(f"Error initializing database: {e}")
        raise
    finally:
        conn.close()