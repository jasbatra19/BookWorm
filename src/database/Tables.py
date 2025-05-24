Books='''CREATE TABLE IF NOT EXISTS books (
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
            maturityRating TEXT,
            recommendedPercentange INTEGER
        )'''

BooksID='''CREATE TABLE IF NOT EXISTS booksId (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            postID INTEGER PRIMARY KEY,
            title TEXT,
            link TEXT,
            score INTEGER,
            num_comments INTEGER
            content TEXT,
            comments TEXT
        )'''