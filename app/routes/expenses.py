from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from datetime import date
from app.models import Expense, ExpenseCreate
from app import crud

router = APIRouter(prefix="/expenses", tags=["Expenses"])


# --- CREATE ---
@router.post("/", response_model=Expense)
def create_expense(expense: ExpenseCreate):
    created = crud.create_expense(expense)
    return created


# --- READ ALL ---
@router.get("/", response_model=List[Expense])
def read_expenses(
    category: Optional[str] = Query(None, description="Фильтр по категории"),
    date_from: Optional[date] = Query(None, description="Начальная дата фильтра"),
    date_to: Optional[date] = Query(None, description="Конечная дата фильтра")
):
    expenses = crud.get_all_expenses(category=category, date_from=date_from, date_to=date_to)
    return expenses


# --- READ ONE ---
@router.get("/{expense_id}", response_model=Expense)
def read_expense(expense_id: int):
    expense = crud.get_expense_by_id(expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Расход не найден")
    return expense


# --- UPDATE ---
@router.put("/{expense_id}", response_model=Expense)
def update_expense(expense_id: int, new_data: ExpenseCreate):
    updated = crud.update_expense(expense_id, new_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Не удалось обновить: расход не найден")
    return updated


# --- DELETE ---
@router.delete("/{expense_id}")
def delete_expense(expense_id: int):
    deleted = crud.delete_expense(expense_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Не удалось удалить: расход не найден")
    return {"ok": True, "message": f"Расход с id={expense_id} удалён"}
