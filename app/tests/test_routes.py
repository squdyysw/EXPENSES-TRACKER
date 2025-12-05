"""
Tests for Expense API routes.
"""

import os
import tempfile
from fastapi.testclient import TestClient
from app.main import app
from app.database import DB_NAME, init_db


def setup_test_db():
    temp_db = tempfile.NamedTemporaryFile(delete=False)
    os.environ["TEST_DB"] = temp_db.name

    global DB_NAME
    DB_NAME = temp_db.name

    init_db()
    return temp_db.name


def teardown_test_db(path):
    os.remove(path)


client = TestClient(app)


def test_create_expense():
    db_file = setup_test_db()

    payload = {
        "title": "Coffee",
        "amount": 4.5,
        "category": "Food"
    }

    response = client.post("/expenses/", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["title"] == "Coffee"
    assert data["amount"] == 4.5
    assert data["category"] == "Food"
    assert "id" in data

    teardown_test_db(db_file)


def test_read_expenses():
    db_file = setup_test_db()

    client.post("/expenses/", json={"title": "Tea", "amount": 2})
    client.post("/expenses/", json={"title": "Burger", "amount": 8})

    response = client.get("/expenses/")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2

    teardown_test_db(db_file)


def test_read_single_expense():
    db_file = setup_test_db()

    created = client.post("/expenses/", json={"title": "Soda", "amount": 3}).json()
    expense_id = created["id"]

    response = client.get(f"/expenses/{expense_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Soda"

    teardown_test_db(db_file)


def test_update_expense():
    db_file = setup_test_db()

    created = client.post("/expenses/", json={"title": "Milk", "amount": 2}).json()
    expense_id = created["id"]

    response = client.put(
        f"/expenses/{expense_id}",
        json={"title": "Milk 2L", "amount": 3}
    )
    assert response.status_code == 200
    data = response.json()

    assert data["title"] == "Milk 2L"
    assert data["amount"] == 3

    teardown_test_db(db_file)


def test_delete_expense():
    db_file = setup_test_db()

    created = client.post("/expenses/", json={"title": "Water", "amount": 1}).json()
    expense_id = created["id"]

    response = client.delete(f"/expenses/{expense_id}")
    assert response.status_code == 200
    assert response.json()["ok"] is True

    not_found = client.get(f"/expenses/{expense_id}")
    assert not_found.status_code == 404

    teardown_test_db(db_file)
