import sqlite3

# Tworzymy bazę danych
conn = sqlite3.connect('biblioteka.db')
cursor = conn.cursor()

# Tworzenie tabel
cursor.execute('''
CREATE TABLE IF NOT EXISTS authors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author_id INTEGER,
    FOREIGN KEY(author_id) REFERENCES authors(id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS loans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER,
    member_id INTEGER,
    loan_date TEXT,
    return_date TEXT,
    FOREIGN KEY(book_id) REFERENCES books(id),
    FOREIGN KEY(member_id) REFERENCES members(id)
)
''')

# Wstawiamy nowych autorów
cursor.execute("INSERT INTO authors (name) VALUES ('Henryk Sienkiewicz')")
cursor.execute("INSERT INTO authors (name) VALUES ('Adam Mickiewicz')")
cursor.execute("INSERT INTO authors (name) VALUES ('Bolesław Prus')")
cursor.execute("INSERT INTO authors (name) VALUES ('Maria Konopnicka')")
cursor.execute("INSERT INTO authors (name) VALUES ('Stanisław Lem')")

# Wstawiamy nowe książki
cursor.execute("INSERT INTO books (title, author_id) VALUES ('W pustyni i w puszczy', 1)")
cursor.execute("INSERT INTO books (title, author_id) VALUES ('Pan Tadeusz', 2)")
cursor.execute("INSERT INTO books (title, author_id) VALUES ('Lalka', 3)")
cursor.execute("INSERT INTO books (title, author_id) VALUES ('Rota', 4)")
cursor.execute("INSERT INTO books (title, author_id) VALUES ('Solaris', 5)")

# Wstawiamy przykładowych członków
cursor.execute("INSERT INTO members (name) VALUES ('Alicja')")
cursor.execute("INSERT INTO members (name) VALUES ('Bartek')")
cursor.execute("INSERT INTO members (name) VALUES ('Celina')")
cursor.execute("INSERT INTO members (name) VALUES ('Damian')")
cursor.execute("INSERT INTO members (name) VALUES ('Ewa')")

# Wstawiamy przykładowe wypożyczenia
cursor.execute("INSERT INTO loans (book_id, member_id, loan_date, return_date) VALUES (1, 1, '2025-06-01', '2025-06-10')")
cursor.execute("INSERT INTO loans (book_id, member_id, loan_date, return_date) VALUES (2, 2, '2025-06-05', NULL)")
cursor.execute("INSERT INTO loans (book_id, member_id, loan_date, return_date) VALUES (3, 3, '2025-06-07', NULL)")
cursor.execute("INSERT INTO loans (book_id, member_id, loan_date, return_date) VALUES (4, 4, '2025-06-08', '2025-06-15')")
cursor.execute("INSERT INTO loans (book_id, member_id, loan_date, return_date) VALUES (5, 5, '2025-06-09', NULL)")

# Zatwierdzamy zmiany
conn.commit()
conn.close()

print("Baza danych z polskimi książkami została utworzona i wypełniona przykładowymi danymi.")
