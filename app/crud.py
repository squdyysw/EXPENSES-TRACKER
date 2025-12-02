"""
CRUD operations for working with the expenses table.

Contains functions for creating, reading, updating, and deleting records.
Uses Pydantic models for strict input and output data validation.
Includes logging and error handling for robust database operations.
"""

from datetime import datetime, date
from typing import Optional, List

from app.database import get_db_connection
from app.models import Expense, ExpenseCreate
from app.logging_info import logger


def create_expense(expense_data: ExpenseCreate) -> Optional[Expense]:
    """
    Create a new expense record in the database.

    Parameters
    ----------
    expense_data : ExpenseCreate
        Validated input data for the expense.

    Returns
    -------
    Expense or None
        The created expense with assigned ID and normalized date.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        date_value = expense_data.date or datetime.now()

        cursor.execute(
            "INSERT INTO expenses (title, amount, category, date) VALUES (?, ?, ?, ?)",
            (expense_data.title, expense_data.amount, expense_data.category, date_value.isoformat())
        )
        conn.commit()
        expense_id = cursor.lastrowid
        logger.info(f"Expense created with ID {expense_id}")
        return Expense(
            id=expense_id,
            title=expense_data.title,
            amount=expense_data.amount,
            category=expense_data.category,
            date=date_value.date()
        )
    except Exception as e:
        logger.error(f"Error creating expense: {e}")
        return None
    finally:
        conn.close()


def get_all_expenses(
    category: Optional[str] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None
) -> List[Expense]:
    """
    Retrieve all expenses with optional filtering.

    Parameters
    ----------
    category : str, optional
        Filter by category.
    date_from : date, optional
        Lower bound for date.
    date_to : date, optional
        Upper bound for date.

    Returns
    -------
    list[Expense]
        A list of expenses matching the filter criteria.
    """
    try:
        conn = get_db_connection()
        query = "SELECT * FROM expenses WHERE 1=1"
        params = []

        if category:
            query += " AND category = ?"
            params.append(category)
        if date_from:
            query += " AND date >= ?"
            params.append(date_from.isoformat())
        if date_to:
            query += " AND date <= ?"
            params.append(date_to.isoformat())

        cursor = conn.execute(query, params)
        rows = cursor.fetchall()
        logger.info(f"Retrieved {len(rows)} expenses from DB")
        return [
            Expense(
                id=row["id"],
                title=row["title"],
                amount=row["amount"],
                category=row["category"],
                date=datetime.fromisoformat(row["date"]).date()
            )
            for row in rows
        ]
    except Exception as e:
        logger.error(f"Error retrieving expenses: {e}")
        return []
    finally:
        conn.close()


def get_expense_by_id(expense_id: int) -> Optional[Expense]:
    """
    Retrieve a single expense by its ID.

    Parameters
    ----------
    expense_id : int
        The ID of the expense to fetch.

    Returns
    -------
    Expense or None
        The expense object if found, otherwise None.
    """
    try:
        conn = get_db_connection()
        row = conn.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,)).fetchone()
        if not row:
            logger.info(f"Expense ID {expense_id} not found")
            return None
        return Expense(
            id=row["id"],
            title=row["title"],
            amount=row["amount"],
            category=row["category"],
            date=datetime.fromisoformat(row["date"]).date()
        )
    except Exception as e:
        logger.error(f"Error retrieving expense ID {expense_id}: {e}")
        return None
    finally:
        conn.close()


def update_expense(expense_id: int, new_data: ExpenseCreate) -> Optional[Expense]:
    """
    Update an existing expense.

    Parameters
    ----------
    expense_id : int
        ID of the expense to update.
    new_data : ExpenseCreate
        New validated data.

    Returns
    -------
    Expense or None
        Updated object, or None if the record does not exist.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        date_value = new_data.date or datetime.now()
        cursor.execute(
            "UPDATE expenses SET title = ?, amount = ?, category = ?, date = ? WHERE id = ?",
            (new_data.title, new_data.amount, new_data.category, date_value.isoformat(), expense_id)
        )
        conn.commit()
        if cursor.rowcount == 0:
            logger.info(f"No expense found with ID {expense_id} to update")
            return None
        logger.info(f"Expense ID {expense_id} updated")
        return Expense(
            id=expense_id,
            title=new_data.title,
            amount=new_data.amount,
            category=new_data.category,
            date=date_value.date()
        )
    except Exception as e:
        logger.error(f"Error updating expense ID {expense_id}: {e}")
        return None
    finally:
        conn.close()


def delete_expense(expense_id: int) -> bool:
    """
    Delete an expense by its ID.

    Parameters
    ----------
    expense_id : int
        ID of the expense to delete.

    Returns
    -------
    bool
        True if a record was deleted, False otherwise.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        conn.commit()
        deleted = cursor.rowcount > 0
        if deleted:
            logger.info(f"Expense ID {expense_id} deleted")
        else:
            logger.info(f"Expense ID {expense_id} not found for deletion")
        return deleted
    except Exception as e:
        logger.error(f"Error deleting expense ID {expense_id}: {e}")
        return False
    finally:
        conn.close()
