import os
import tempfile
import pytest
from fastapi.testclient import TestClient

from app.main import app
import app.database as db

os.environ["TESTING"] = "1"


@pytest.fixture(scope="session", autouse=True)
def test_database():
    """
    Creates a temporary SQLite DB file and forces the entire app
    to use it during all tests.
    """

    temp_db = tempfile.NamedTemporaryFile(delete=False)
    temp_db.close()

    original_name = db.DB_NAME

    db.DB_NAME = temp_db.name

    db.init_db()

    yield

    os.remove(temp_db.name)
    db.DB_NAME = original_name


@pytest.fixture
def client():
    """
    Returns FastAPI TestClient using the injected test DB.
    """
    return TestClient(app)

