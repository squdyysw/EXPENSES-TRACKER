"""
API routes for managing expenses.

Includes endpoints for creating, reading, updating, and deleting expenses.
Adds logging and error handling for all operations.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from datetime import date
from app.models import Expense, ExpenseCreate
from app import crud
from app.logging_info import logger

router = APIRouter(prefix="/expenses", tags=["Expenses"])


@router.post("/", response_model=Expense)
def create_expense(expense: ExpenseCreate):
    """
    Create a new expense entry.

    :param expense: Incoming expense payload.
    :return: Created Expense object.
    """
    try:
        created = crud.create_expense(expense)
        if not created:
            logger.error("Failed to create expense")
            raise HTTPException(status_code=500, detail="Failed to create expense")
        logger.info(f"Expense created with ID {created.id}")
        return created
    except Exception as e:
        logger.error(f"Exception in create_expense: {e}")
        raise HTTPException(status_code=500, detail=str(e))


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
    try:
        expenses = crud.get_all_expenses(category=category, date_from=date_from, date_to=date_to)
        logger.info(f"Retrieved {len(expenses)} expenses")
        return expenses
    except Exception as e:
        logger.error(f"Exception in read_expenses: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{expense_id}", response_model=Expense)
def read_expense(expense_id: int):
    """
    Retrieve a single expense by ID.

    :param expense_id: Target expense ID.
    :return: Expense object if found.
    :raises HTTPException: If entry doesn't exist.
    """
    try:
        expense = crud.get_expense_by_id(expense_id)
        if not expense:
            logger.info(f"Expense ID {expense_id} not found")
            raise HTTPException(status_code=404, detail="Expense not found")
        logger.info(f"Retrieved expense ID {expense_id}")
        return expense
    except Exception as e:
        logger.error(f"Exception in read_expense: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{expense_id}", response_model=Expense)
def update_expense(expense_id: int, new_data: ExpenseCreate):
    """
    Update an existing expense.

    :param expense_id: ID of the expense to update.
    :param new_data: Updated values.
    :return: Updated Expense object.
    :raises HTTPException: If entry doesn't exist.
    """
    try:
        updated = crud.update_expense(expense_id, new_data)
        if not updated:
            logger.info(f"Expense ID {expense_id} not found for update")
            raise HTTPException(status_code=404, detail="Expense not found")
        logger.info(f"Expense ID {expense_id} updated")
        return updated
    except Exception as e:
        logger.error(f"Exception in update_expense: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{expense_id}")
def delete_expense(expense_id: int):
    """
    Delete an expense by ID.

    :param expense_id: Target expense ID.
    :return: JSON confirmation message.
    :raises HTTPException: If entry doesn't exist.
    """
    try:
        deleted = crud.delete_expense(expense_id)

        if not deleted:
            logger.info(f"Expense {expense_id} not found")
            raise HTTPException(status_code=404, detail="Expense not found")

        logger.info(f"Expense {expense_id} deleted")
        return {"ok": True, "message": f"Expense id={expense_id} deleted"}

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Exception in delete_expense: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
