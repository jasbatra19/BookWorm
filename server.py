from fastapi import FastAPI,Query
from fastapi.middleware.cors import CORSMiddleware
from src.api.get_api import HelloBookWorms
from typing import Optional
from datetime import datetime
from src.plugins.reddit.reddit_scraper import get_reddit_recommendations
from src.database.bookStore import *

app= FastAPI()
origins = [
    "http://localhost:3002",  # React app running here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],      # or restrict to ["GET", "POST"] etc.
    allow_headers=["*"],      # or restrict to specific headers
)

create_table_books()
create_table_booksId()
create_junction_book_post_map()

client=HelloBookWorms()

@app.get('/author/{author_name}')
def get_author(author_name:str):
    print('getting book by author name')
    return client.get_author(author_name=author_name)
    
@app.get('/title/{title}')
def get_by_title(title:str):
    print('getting book by title')
    return client.get_by_title(title_name=title)

@app.get('/genre/{genre}')
def get_by_genre(genre:str):
    print('getting book by genre')
    return client.get_genre(genre=genre)

@app.get('/bestseller/{top}')
async def get_bestSellers(top:int):
    print('getting topseller books')
    return await client.get_bestsellers(limit=top)

@app.get('/newReleases')
def get_bestSellers(top: Optional[int] = 10, year: Optional[int] = None, month: Optional[int] = None):
    year = year if year is not None else datetime.now().year
    month = month if month is not None else datetime.now().month
    print('getting new releases')
    return client.get_new_releases_by_year_or_month(limit=top, year=year, month=month)

@app.get('/reddit_recommendations')
async def reddit_recommendation():
    recommendations=[]
    print('getting reddit recommended book')
    books=get_reddit_recommendations()
    booksBatch = await client.batch_fetch_books(books)
    # check if similar book exists in db 
    # {
        #     "bookId": "kcVlAAAAMAAJ",
        #     "title": "Waltzing Again",
        #     "author": "Margaret Atwood",
        #     "description": "\"\"I don't mind being 'interviewed' any more than I mind Viennese waltzing--that is, my response will depend on the agility and grace and attitude and intelligence of the other person. Some do it well, some clumsily, some step on your toes by accident, and some aim for them.\"\"--Margaret Atwood This gathering of 21 interviews with Margaret Atwood covers a broad spectrum of topics. Beginning with Graeme Gibson's \"Dissecting the Way a Writer Works\" (1972), the conversations provide a forum for Atwood to talk about her own work, her career as a writer, feminism, and Canadian cultural nationalism, and to refute the autobiographical fallacy. These conversations offer what Earl Ingersoll calls \"a kind of 'biography' of Margaret Atwood--the only kind of biography she is likely to sanction.\" Enlivened by Atwood's unfailing sense of humor, the interviews present an invaluable view of a distinguished contemporary writer at work. From the Interviews: \"\"Let's not pretend that the interview will necessarily result in any absolute and blinding revelations. Interviews too are an art form; that is to say, they indulge in the science of illusion.\" \"I don't think you ever know how to write a book. You never know ahead of time. You start every time at zero. A former success doesn't mean that you're not going to make the most colossal failure the next time.\"\"",
        #     "publishedDate": "2006",
        #     "pageCount": 312,
        #     "averageRating": 4,
        #     "ratingsCount": 1,
        #     "categories": [
        #         "Biography & Autobiography"
        #     ],
        #     "thumbnail": "http://books.google.com/books/content?id=kcVlAAAAMAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api",
        #     "maturityRating": "NOT_MATURE",
        #     "previewLink": "http://books.google.co.in/books?id=kcVlAAAAMAAJ&q=intitle:Margaret+Atwood&dq=intitle:Margaret+Atwood&hl=&cd=1&source=gbs_api"
        # },
    for bookList in booksBatch:
        for book in bookList:
            print(book['title'])  # or just print(book)
            # if get_book_by_ID(book['bookId']):
                # updateBooksRecommendedPercentage(book['bookId'])
            # else:
                # insert_book(book)

        
    # if yes retrieve that update recom%
    # if not make a seperate list 
    # batch update for the db and api
    # we keep the most voted/ rec% in cache for quick retrieval


    return recommendations

@app.get('/getAllBooks')
def get_books_from_db():
    books=get_all_books()
    return books



