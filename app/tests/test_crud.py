import os
import tempfile
import pytest

import app.database as db
from app import crud
from app.models import ExpenseCreate

@pytest.fixture
def test_db():
    temp_db = tempfile.NamedTemporaryFile(delete=False)
    temp_db.close()
    original_db_name = db.DB_NAME
    db.DB_NAME = temp_db.name
    db.init_db()
    yield db.DB_NAME
    os.remove(temp_db.name)
    db.DB_NAME = original_db_name

def test_create_expense(test_db):
    new_expense = ExpenseCreate(title="Test", amount=100.0, category="Food", date=None)
    result = crud.create_expense(new_expense)
    assert result is not None
    assert result.id == 1
    assert result.title == "Test"
    assert result.amount == 100.0
    assert result.category == "Food"

def test_get_expense_by_id(test_db):
    exp = ExpenseCreate(title="Coffee", amount=5, category="Food")
    created = crud.create_expense(exp)
    fetched = crud.get_expense_by_id(created.id)
    assert fetched is not None
    assert fetched.title == "Coffee"

def test_update_expense(test_db):
    exp = ExpenseCreate(title="Old", amount=10, category="Other")
    created = crud.create_expense(exp)
    updated = crud.update_expense(created.id, ExpenseCreate(title="New", amount=20, category="Bills"))
    assert updated.title == "New"
    assert updated.amount == 20
    assert updated.category == "Bills"

def test_delete_expense(test_db):
    exp = ExpenseCreate(title="Delete", amount=9, category="Other")
    created = crud.create_expense(exp)
    deleted = crud.delete_expense(created.id)
    assert deleted is True
    assert crud.get_expense_by_id(created.id) is None
