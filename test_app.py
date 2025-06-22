import sqlite3
import os

DB_NAME = 'biblioteka.db'

def test_database_connection():
    assert os.path.exists(DB_NAME), f"Plik bazy danych {DB_NAME} nie istnieje."
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    conn.close()
    assert len(tables) >= 2, "Baza powinna zawierać co najmniej 2 tabele."
