Books='''CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bookId TEXT,
            title TEXT,
            author TEXT,
            description TEXT,
            publishedDate TEXT,
            pageCount INTEGER,
            averageRating REAL,
            ratingsCount INTEGER,
            categories TEXT,
            thumbnail TEXT,
            maturityRating TEXT,
            recommendedPercentage INTEGER DEFAULT 1,
            dateOfProcessing DATE
        )'''

BooksID='''CREATE TABLE IF NOT EXISTS booksId (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            postID TEXT,
            title TEXT,
            link TEXT,
            score INTEGER,
            num_comments INTEGER,
            content TEXT,
            comments TEXT
        )'''

BookPostMap='''CREATE TABLE IF NOT EXISTS book_post_map (
    book_id INTEGER,
    post_id INTEGER,
    FOREIGN KEY(book_id) REFERENCES books(id),
    FOREIGN KEY(post_id) REFERENCES booksId(id),
    PRIMARY KEY (book_id, post_id)
)'''
