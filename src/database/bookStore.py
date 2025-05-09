import sqlite3

DB_PATH = 'books.db'

def connect_db():
    return sqlite3.connect(DB_PATH)

def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            description TEXT,
            publishedDate TEXT,
            pageCount INTEGER,
            averageRating REAL,
            ratingsCount INTEGER,
            categories TEXT,
            thumbnail TEXT,
            maturityRating TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_book(book):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM books where title = ? and author= ?
''',(book['title'],book['author']))
    existing = cursor.fetchone()
    if existing:
        print('book already exists in the database.')
    else:
        cursor.execute('''
            INSERT INTO books (
                title, author, description, publishedDate, pageCount,
                averageRating, ratingsCount, categories, thumbnail,
                maturityRating
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            book['title'],
            book['author'],
            book['description'],
            book['publishedDate'],
            book['pageCount'],
            book['averageRating'],
            book['ratingsCount'],
            ', '.join(book['categories']),
            book['thumbnail'],
            book['maturityRating']
        ))
        conn.commit()
    conn.close()

def get_all_books():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_book_by_name(book):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE title = ?", (book,))
    rows = cursor.fetchall()
    conn.close()
    return rows
