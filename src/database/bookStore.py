import sqlite3
from src.database.Tables import Books, BooksID, BookPostMap
DB_PATH = 'books.db'

def connect_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

# creates table containg books information which is required to be displayed  
def create_table_books():
    '''create tables in books schema'''
    conn = connect_db()
    # table - BOOKS
    cursor = conn.cursor()
    cursor.execute(Books)
    conn.commit()
    conn.close()

#  creates table to store posts and its meta data
def create_table_booksId():
    '''create tables in BookId schema'''
    conn = connect_db()
    # table - BOOKSID
    cursor = conn.cursor()
    cursor.execute(BooksID)
    conn.commit()
    conn.close()

# create a junction to store many to many reln between books and post
def create_junction_book_post_map():
    '''create table in BookPostMap schema - handles many to many reln'''
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(BookPostMap)
    conn.commit()
    conn.close()


# check for post id if already exists
def existing_ids(post_id):
    '''check if the current post is already in DB'''
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM booksId where postId = ?
    ''',(post_id,))
    existing = cursor.fetchone()
    if existing:
        print('book already exists in the database.')
        return True
    conn.commit()
    conn.close()
    return False


# inserts into booksId post id and metadata
def post_info(post_data):
    '''Stores post information in booksId table'''
    conn=connect_db()
    cursor=conn.cursor()
    cursor.execute('''
    INSERT INTO booksId(postId,title,link,score,num_comments,content,comments) VALUES (?,?,?,?,?,?,?)
    ''',(
    post_data["id"],
    post_data["title"],
    post_data["link"],
    post_data["score"],
    post_data["num_comments"],
    post_data["content"],
    str(post_data["comments"])
))
    conn.commit()
    conn.close()

# inserts into books the books information fetched from google books API
def insert_book(book):
    '''Insert book into books'''
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
            INSERT INTO books (
                bookId,title, author, description, publishedDate, pageCount,
                averageRating, ratingsCount, categories, thumbnail,
                maturityRating,dateOfProcessing
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,CURRENT_DATE)
        ''', (
            book['bookId'],
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
    print('book inserted into the database')
    conn.commit()
    conn.close()





# fetches all the books in the books db
def get_all_books():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_book_by_ID(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books where bookId= ?",id)
    rows = cursor.fetchall()
    conn.close()
    return rows




#  fetches books by its title
def get_book_by_name(book):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE title = ?", (book,))
    rows = cursor.fetchall()
    conn.close()
    return rows

#  updated recommendations if the book is present in some other post as well
def updateBooksRecommendedPercentage(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE books SET recommendedPercentage = COALESCE(recommendedPercentage, 0) + 1, dateOfProcessing = CURRENT_DATE
    WHERE bookId = ?
''',id)
    print('book already exists in the database. recommendedPercentage of recommendation updated ')

    conn.commit()
    affected_rows = cursor.rowcount  # Number of rows updated
    conn.close()
    return affected_rows


def map_book_to_post(book_id, post_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO book_post_map (book_id, post_id) VALUES (?, ?)
    ''', (book_id, post_id))
    conn.commit()
    conn.close()

def get_books_from_post(post_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT b.* FROM books b
        JOIN book_post_map m ON b.id = m.book_id
        WHERE m.post_id = ?
    ''', (post_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_posts_from_book(book_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT p.* FROM booksId p
        JOIN book_post_map m ON p.id = m.post_id
        WHERE m.book_id = ?
    ''', (book_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows
