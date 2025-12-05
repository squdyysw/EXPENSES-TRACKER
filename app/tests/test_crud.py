from app import crud
from app.models import ExpenseCreate


def test_create_expense():
    new_expense = ExpenseCreate(
        title="Test",
        amount=100.0,
        category="Food",
        date=None
    )

    result = crud.create_expense(new_expense)

    assert result.id == 1
    assert result.title == "Test"
    assert result.amount == 100.0
    assert result.category == "Food"


def test_get_expense_by_id():
    exp = ExpenseCreate(title="Coffee", amount=5, category="Food")

    created = crud.create_expense(exp)
    fetched = crud.get_expense_by_id(created.id)

    assert fetched is not None
    assert fetched.title == "Coffee"


def test_update_expense():
    exp = ExpenseCreate(title="Old", amount=10, category="Other")
    created = crud.create_expense(exp)

    updated = crud.update_expense(
        created.id,
        ExpenseCreate(title="New", amount=20, category="Bills")
    )

    assert updated.title == "New"
    assert updated.amount == 20
    assert updated.category == "Bills"


def test_delete_expense():
    exp = ExpenseCreate(title="Delete", amount=9, category="Other")
    created = crud.create_expense(exp)

    deleted = crud.delete_expense(created.id)
    assert deleted is True

    assert crud.get_expense_by_id(created.id) is None
