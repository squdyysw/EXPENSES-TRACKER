import os
import tempfile
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.database import DB_NAME, init_db


@pytest.fixture(scope="session", autouse=True)
def test_database():
    """
    Create a temporary SQLite file DB for all tests.
    This avoids issues with :memory: creating separate DB per connection.
    """
    # создаём временный файл
    temp_db = tempfile.NamedTemporaryFile(delete=False)
    temp_db.close()

    # подменяем имя БД
    original_name = DB_NAME
    os.environ["TEST_DB_NAME"] = temp_db.name

    # меняем глобальное имя в модуле
    import app.database as db
    db.DB_NAME = temp_db.name

    # инициализируем таблицы
    init_db()

    yield

    # удаляем временную БД после тестов
    os.remove(temp_db.name)
    db.DB_NAME = original_name


@pytest.fixture
def client():
    return TestClient(app)
