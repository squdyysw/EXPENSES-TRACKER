from app.database import get_db_connection
from app.models import Expense, ExpenseCreate
from datetime import datetime, date
from typing import Optional, List


# --- CREATE ---
def create_expense(expense_data: ExpenseCreate) -> Expense:
    conn = get_db_connection()
    cursor = conn.cursor()

    now = datetime.now()
    date_value = expense_data.date or now

    cursor.execute(
        "INSERT INTO expenses (title, amount, category, date) VALUES (?, ?, ?, ?)",
        (expense_data.title, expense_data.amount, expense_data.category, date_value.isoformat())
    )
    conn.commit()

    expense_id = cursor.lastrowid
    conn.close()

    return Expense(
        id=expense_id,
        title=expense_data.title,
        amount=expense_data.amount,
        category=expense_data.category,
        date=date_value.date()
    )


# --- READ ---
def get_all_expenses(
    category: Optional[str] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None
) -> List[Expense]:
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
    conn.close()

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


def get_expense_by_id(expense_id: int) -> Optional[Expense]:
    conn = get_db_connection()
    row = conn.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,)).fetchone()
    conn.close()

    if not row:
        return None

    return Expense(
        id=row["id"],
        title=row["title"],
        amount=row["amount"],
        category=row["category"],
        date=datetime.fromisoformat(row["date"]).date()
    )


# --- UPDATE ---
def update_expense(expense_id: int, new_data: ExpenseCreate) -> Optional[Expense]:
    conn = get_db_connection()
    cursor = conn.cursor()

    date_value = new_data.date or datetime.now()
    cursor.execute(
        "UPDATE expenses SET title = ?, amount = ?, category = ?, date = ? WHERE id = ?",
        (new_data.title, new_data.amount, new_data.category, date_value.isoformat(), expense_id)
    )

    conn.commit()
    updated = cursor.rowcount > 0
    conn.close()

    if not updated:
        return None

    return Expense(
        id=expense_id,
        title=new_data.title,
        amount=new_data.amount,
        category=new_data.category,
        date=date_value.date()
    )


# --- DELETE ---
def delete_expense(expense_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted
