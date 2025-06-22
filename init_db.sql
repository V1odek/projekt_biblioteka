DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS authors;

CREATE TABLE authors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author_id INTEGER,
    FOREIGN KEY (author_id) REFERENCES authors(id)
);

INSERT INTO authors (name) VALUES 
('Henryk Sienkiewicz'),
('Adam Mickiewicz'),
('Bolesław Prus'),
('Maria Konopnicka'),
('Stanisław Lem');

INSERT INTO books (title, author_id) VALUES 
('W pustyni i w puszczy', 1),
('Pan Tadeusz', 2),
('Lalka', 3),
('Rota', 4),
('Solaris', 5);
