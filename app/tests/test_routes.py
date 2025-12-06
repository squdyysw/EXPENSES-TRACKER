import os
import tempfile
import pytest
from fastapi.testclient import TestClient
import app.database as db
from app.main import app

@pytest.fixture(scope="function")
def test_client():
    temp_db = tempfile.NamedTemporaryFile(delete=False)
    temp_db.close()

    original_db_name = db.DB_NAME
    db.DB_NAME = temp_db.name
    db.init_db()

    client = TestClient(app)
    yield client

    os.remove(temp_db.name)
    db.DB_NAME = original_db_name

def test_create_expense(test_client):
    payload = {"title": "Coffee", "amount": 4.5, "category": "Food"}
    response = test_client.post("/expenses/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Coffee"
    assert data["amount"] == 4.5
    assert data["category"] == "Food"
    assert "id" in data

def test_read_expenses(test_client):
    test_client.post("/expenses/", json={"title": "Tea", "amount": 2})
    test_client.post("/expenses/", json={"title": "Burger", "amount": 8})
    response = test_client.get("/expenses/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2

def test_read_single_expense(test_client):
    created = test_client.post("/expenses/", json={"title": "Soda", "amount": 3}).json()
    expense_id = created["id"]
    response = test_client.get(f"/expenses/{expense_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Soda"

def test_update_expense(test_client):
    created = test_client.post("/expenses/", json={"title": "Milk", "amount": 2}).json()
    expense_id = created["id"]
    response = test_client.put(f"/expenses/{expense_id}", json={"title": "Milk 2L", "amount": 3})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Milk 2L"
    assert data["amount"] == 3

def test_delete_expense(test_client):
    created = test_client.post("/expenses/", json={"title": "Water", "amount": 1}).json()
    expense_id = created["id"]
    response = test_client.delete(f"/expenses/{expense_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["ok"] is True
    not_found = test_client.get(f"/expenses/{expense_id}")
    assert not_found.status_code == 404
