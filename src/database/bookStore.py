import sqlite3
from src.database.Tables import Books, BooksID
DB_PATH = 'books.db'

def connect_db():
    return sqlite3.connect(DB_PATH)

def create_table():
    '''create tables in books schema'''
    conn = connect_db()
    # table - BOOKS
    cursor = conn.cursor()
    cursor.execute(Books)
    conn.commit()
    # table - BOOKSID
    conn.cursor()
    cursor.execute(BooksID)
    conn.commit()
    conn.close()


def existing_ids(post_id):
    '''check if the current post is already in DB'''
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM booksId where postId = ? a
    ''',(post_id))
    existing = cursor.fetchone()
    if existing:
        print('book already exists in the database.')
        return True
    conn.commit()
    conn.close()
    return False



def post_info(post_data):
    '''Stores post information in booksId table'''
    conn=connect_db()
    cursor=conn.cursor()
    cursor.execute('''
    INSERT INTO booksId(postId,title,link,score,num_comments,content,comments) VALUES (?,?,?,?,?)
    ''',(
    post_data.id,
    post_data.title,
    post_data.link,
    post_data.score,
    post_data.num_comments,
    post_data.content,
    post_data.comments
))

    conn.commit()
    conn.close()


def insert_book(book):
    '''Insert book into books'''
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM books where title = ? and author= ?
    ''',(book['title'],book['author']))
    existing = cursor.fetchone()
    if existing:
        cursor.execute('''
        UPDATE books SET recommendedPercentange = COALESCE(recommendedPercentage, 0) + 1
        WHERE id = ?
    ''',existing['id'])
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
