import os
from database import get_db_connection

DB_PATH = "expenses.db"


def clear_table():
    """
    Delete all records from the 'expenses' table.

    This function connects to the SQLite database using the shared
    connection factory, executes a DELETE statement to remove all rows
    from the 'expenses' table, commits the transaction, and closes
    the connection.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses")
    conn.commit()
    conn.close()
    print("✅ Все записи в таблице 'expenses' удалены.")


def drop_database():
    """
    Remove the SQLite database file entirely.

    If the file referenced by DB_PATH exists, it is deleted.
    Otherwise, a notification is printed that no database file was found.
    """
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"🗑️ База данных '{DB_PATH}' удалена.")
    else:
        print("⚠️ Файл базы данных не найден.")


if name == "__main__":
    print("Выберите действие:")
    print("1. Очистить таблицу 'expenses'")
    print("2. Полностью удалить базу данных")
    choice = input("👉 Введите 1 или 2: ")

    if choice == "1":
        clear_table()
    elif choice == "2":
        drop_database()
    else:
        print("❌ Неверный выбор.")
