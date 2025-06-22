import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import sqlite3
import csv

DB_NAME = 'biblioteka.db'

def get_authors():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM authors")
    authors = cursor.fetchall()
    conn.close()
    return authors

def show_records(rows=None):
    for row in tree.get_children():
        tree.delete(row)

    if rows is None:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT books.id, books.title, authors.name
            FROM books
            LEFT JOIN authors ON books.author_id = authors.id
        ''')
        rows = cursor.fetchall()
        conn.close()

    for row in rows:
        tree.insert("", tk.END, values=row)

def add_book():
    title = entry_title.get()
    author_id = combo_author.get()

    if not title or not author_id:
        messagebox.showwarning("Brak danych", "Wpisz tytuł i wybierz autora.")
        return

    author_id = int(author_id.split(":")[0])

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (title, author_id) VALUES (?, ?)", (title, author_id))
    conn.commit()
    conn.close()

    messagebox.showinfo("Sukces", f"Książka '{title}' została dodana.")
    entry_title.delete(0, tk.END)
    show_records()

def delete_book():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Brak wyboru", "Zaznacz książkę do usunięcia.")
        return

    book_id = tree.item(selected[0])["values"][0]

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    conn.close()

    messagebox.showinfo("Sukces", f"Książka o ID {book_id} została usunięta.")
    show_records()

def load_book_for_edit():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Brak wyboru", "Zaznacz książkę do edycji.")
        return

    book_id, title, author = tree.item(selected[0])["values"]
    entry_title.delete(0, tk.END)
    entry_title.insert(0, title)

    for value in combo_author["values"]:
        if value.endswith(author):
            combo_author.set(value)
            break

    entry_title.book_id = book_id

def save_edited_book():
    if not hasattr(entry_title, 'book_id'):
        messagebox.showwarning("Brak edycji", "Najpierw załaduj książkę do edycji.")
        return

    book_id = entry_title.book_id
    title = entry_title.get()
    author_id = combo_author.get()

    if not title or not author_id:
        messagebox.showwarning("Brak danych", "Wpisz tytuł i wybierz autora.")
        return

    author_id = int(author_id.split(":")[0])

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE books SET title = ?, author_id = ? WHERE id = ?", (title, author_id, book_id))
    conn.commit()
    conn.close()

    messagebox.showinfo("Sukces", f"Książka o ID {book_id} została zaktualizowana.")
    show_records()

    del entry_title.book_id
    entry_title.delete(0, tk.END)
    combo_author.set('')

def search_books():
    query = entry_search.get()
    if not query:
        show_records()
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT books.id, books.title, authors.name
        FROM books
        LEFT JOIN authors ON books.author_id = authors.id
        WHERE books.title LIKE ? OR authors.name LIKE ?
    ''', (f"%{query}%", f"%{query}%"))
    rows = cursor.fetchall()
    conn.close()

    show_records(rows)

def sort_by_title():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT books.id, books.title, authors.name
        FROM books
        LEFT JOIN authors ON books.author_id = authors.id
        ORDER BY books.title
    ''')
    rows = cursor.fetchall()
    conn.close()

    show_records(rows)

def sort_by_author():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT books.id, books.title, authors.name
        FROM books
        LEFT JOIN authors ON books.author_id = authors.id
        ORDER BY authors.name
    ''')
    rows = cursor.fetchall()
    conn.close()

    show_records(rows)

def export_to_csv():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT books.id, books.title, authors.name
        FROM books
        LEFT JOIN authors ON books.author_id = authors.id
    ''')
    rows = cursor.fetchall()
    conn.close()

    with open('biblioteka_eksport.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['ID', 'Tytuł', 'Autor'])
        writer.writerows(rows)

    messagebox.showinfo("Eksport zakończony", "Dane zostały zapisane do pliku biblioteka_eksport.csv")

def import_from_csv():
    filepath = filedialog.askopenfilename(
        title="Wybierz plik CSV",
        filetypes=[("CSV files", "*.csv")]
    )
    if not filepath:
        return

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
    except Exception as e:
        messagebox.showerror("Błąd", f"Błąd przy otwieraniu pliku: {e}")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    for row in rows:
        title = row.get('Tytuł')
        author = row.get('Autor')

        if not title or not author:
            continue

        cursor.execute("SELECT id FROM authors WHERE name = ?", (author,))
        result = cursor.fetchone()

        if result:
            author_id = result[0]
        else:
            cursor.execute("INSERT INTO authors (name) VALUES (?)", (author,))
            author_id = cursor.lastrowid

        cursor.execute("INSERT INTO books (title, author_id) VALUES (?, ?)", (title, author_id))

    conn.commit()
    conn.close()

    messagebox.showinfo("Import zakończony", f"Dane z pliku {filepath} zostały zaimportowane.")
    show_records()

# GUI
root = tk.Tk()
root.title("Biblioteka")

tree = ttk.Treeview(root, columns=("ID", "Tytuł", "Autor"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Tytuł", text="Tytuł")
tree.heading("Autor", text="Autor")
tree.pack(fill=tk.BOTH, expand=True)

form_frame = tk.Frame(root)
form_frame.pack(fill=tk.X, pady=5)

tk.Label(form_frame, text="Tytuł:").pack(side=tk.LEFT, padx=5)
entry_title = tk.Entry(form_frame)
entry_title.pack(side=tk.LEFT, padx=5)

tk.Label(form_frame, text="Autor:").pack(side=tk.LEFT, padx=5)
combo_author = ttk.Combobox(form_frame, values=[
    f"{aid}: {aname}" for aid, aname in get_authors()
], state="readonly")
combo_author.pack(side=tk.LEFT, padx=5)

btn_add = tk.Button(form_frame, text="Dodaj książkę", command=add_book)
btn_add.pack(side=tk.LEFT, padx=5)

search_frame = tk.Frame(root)
search_frame.pack(fill=tk.X, pady=5)

tk.Label(search_frame, text="Szukaj:").pack(side=tk.LEFT, padx=5)
entry_search = tk.Entry(search_frame)
entry_search.pack(side=tk.LEFT, padx=5)

btn_search = tk.Button(search_frame, text="Szukaj", command=search_books)
btn_search.pack(side=tk.LEFT, padx=5)

btn_frame = tk.Frame(root)
btn_frame.pack(fill=tk.X)

btn_show = tk.Button(btn_frame, text="Wyświetl książki", command=show_records)
btn_show.pack(side=tk.LEFT, padx=5, pady=5)

btn_delete = tk.Button(btn_frame, text="Usuń książkę", command=delete_book)
btn_delete.pack(side=tk.LEFT, padx=5, pady=5)

btn_load_edit = tk.Button(btn_frame, text="Edytuj książkę", command=load_book_for_edit)
btn_load_edit.pack(side=tk.LEFT, padx=5, pady=5)

btn_save_edit = tk.Button(btn_frame, text="Zapisz zmiany", command=save_edited_book)
btn_save_edit.pack(side=tk.LEFT, padx=5, pady=5)

btn_sort_title = tk.Button(btn_frame, text="Sortuj według tytułu", command=sort_by_title)
btn_sort_title.pack(side=tk.LEFT, padx=5, pady=5)

btn_sort_author = tk.Button(btn_frame, text="Sortuj według autora", command=sort_by_author)
btn_sort_author.pack(side=tk.LEFT, padx=5, pady=5)

btn_export = tk.Button(btn_frame, text="Eksportuj do CSV", command=export_to_csv)
btn_export.pack(side=tk.LEFT, padx=5, pady=5)

btn_import = tk.Button(btn_frame, text="Importuj z CSV", command=import_from_csv)
btn_import.pack(side=tk.LEFT, padx=5, pady=5)

show_records()
root.mainloop()
