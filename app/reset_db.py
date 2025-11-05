import os
import sqlite3
from database import get_db_connection

DB_PATH = "exspenses.db"  # если твоя база называется иначе — поменяй здесь

def clear_table():
    """Удаляет все данные из таблицы expenses"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses")
    conn.commit()
    conn.close()
    print("✅ Все записи в таблице 'expenses' удалены.")

def drop_database():
    """Полностью удаляет файл базы данных"""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"🗑️ База данных '{DB_PATH}' удалена.")
    else:
        print("⚠️ Файл базы данных не найден.")

if __name__ == "__main__":
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
