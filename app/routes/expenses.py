from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from datetime import date
from app.models import Expense, ExpenseCreate
from app import crud

router = APIRouter(prefix="/expenses", tags=["Expenses"])


@router.post("/", response_model=Expense)
def create_expense(expense: ExpenseCreate):
    """
    Create a new expense entry.

    :param expense: Incoming expense payload.
    :return: Created Expense object.
    """
    return crud.create_expense(expense)


@router.get("/", response_model=List[Expense])
def read_expenses(
    category: Optional[str] = Query(None, description="Filter by category"),
    date_from: Optional[date] = Query(None, description="Filter start date"),
    date_to: Optional[date] = Query(None, description="Filter end date"),
):
    """
    Retrieve a list of expenses with optional filters.

    :param category: Filter by category name.
    :param date_from: Start of date filter.
    :param date_to: End of date filter.
    :return: List of Expense objects.
    """
    return crud.get_all_expenses(
        category=category,
        date_from=date_from,
        date_to=date_to
    )


@router.get("/{expense_id}", response_model=Expense)
def read_expense(expense_id: int):
    """
    Retrieve a single expense by ID.

    :param expense_id: Target expense ID.
    :return: Expense object if found.
    :raises HTTPException: If entry doesn't exist.
    """
    expense = crud.get_expense_by_id(expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


@router.put("/{expense_id}", response_model=Expense)
def update_expense(expense_id: int, new_data: ExpenseCreate):
    """
    Update an existing expense.

    :param expense_id: ID of the expense to update.
    :param new_data: Updated values.
    :return: Updated Expense object.
    :raises HTTPException: If entry doesn't exist.
    """
    updated = crud.update_expense(expense_id, new_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Expense not found")
    return updated


@router.delete("/{expense_id}")
def delete_expense(expense_id: int):
    """
    Delete an expense by ID.

    :param expense_id: Target expense ID.
    :return: JSON confirmation message.
    :raises HTTPException: If entry doesn't exist.
    """
    deleted = crud.delete_expense(expense_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Expense not found")
    return {"ok": True, "message": f"Expense id={expense_id} deleted"}
