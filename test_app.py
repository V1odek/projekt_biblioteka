import sqlite3
import os

DB_NAME = 'biblioteka.db'

def test_database_connection():
    """Sprawdza, czy baza danych istnieje i zawiera co najmniej 2 tabele."""
    assert os.path.exists(DB_NAME), f"Plik bazy danych {DB_NAME} nie istnieje."
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    conn.close()
    assert len(tables) >= 2, "Baza powinna zawierać co najmniej 2 tabele."

def test_add_book():
    """Sprawdza, czy można dodać książkę do bazy danych."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Dodaj książkę testową
    cursor.execute("INSERT INTO books (title, author_id) VALUES (?, ?)", ("Testowa książka", 1))
    conn.commit()
    
    # Sprawdź, czy została dodana
    cursor.execute("SELECT * FROM books WHERE title = ?", ("Testowa książka",))
    result = cursor.fetchone()
    assert result is not None, "Książka nie została dodana do bazy danych."
    
    # Sprzątnij po sobie (usuń testowy rekord)
    cursor.execute("DELETE FROM books WHERE title = ?", ("Testowa książka",))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    test_database_connection()
    print("✅ Test połączenia z bazą danych przeszedł pomyślnie.")
    test_add_book()
    print("✅ Test dodania książki przeszedł pomyślnie.")
