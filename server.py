from fastapi import FastAPI,Query
import uvicorn
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from src.api.get_api import HelloBookWorms
from typing import Optional
from datetime import datetime
from src.database.bookStore import *
import os


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_table_books()
    create_table_booksId()
    create_junction_book_post_map()
    yield

app = FastAPI(lifespan=lifespan)


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


client=HelloBookWorms()

@app.get('/books/search')
def get_books(
    author:Optional[str]=None,
    title:Optional[str]=None,
    genre:Optional[str]=None,
    limit:Optional[int]=Query(default=None,gt=0),
):
    result = []
    if author:
        result+=client.get_author(author_name=author)
    if title:
        result+=client.get_by_title(title_name=title)
    if genre:
        result+=client.get_genre(genre=genre)
    if limit:
        if limit<len(result):
            result = result[:limit]
    return result

    
# @app.get('/author/{author_name}')
# def get_author(author_name:str):
#     print('getting book by author name')
#     return client.get_author(author_name=author_name)
    
# @app.get('/title/{title}')
# def get_by_title(title:str):
#     print('getting book by title')
#     return client.get_by_title(title_name=title)

# @app.get('/genre/{genre}')
# def get_by_genre(genre:str):
#     print('getting book by genre')
#     return client.get_genre(genre=genre)

# @app.get('/bestseller')
# async def get_bestSellers(top:int):
#     print('getting topseller books')
#     return await client.get_bestsellers(limit=top)

# @app.get('/newReleases')
# def get_bestSellers(top: Optional[int] = 10, year: Optional[int] = None, month: Optional[int] = None):
#     year = year if year is not None else datetime.now().year
#     month = month if month is not None else datetime.now().month
#     print('getting new releases')
#     return client.get_new_releases_by_year_or_month(limit=top, year=year, month=month)

@app.get('/recommendations/reddit')
async def reddit_recommendation():
    booksBatch = await client.get_reddit_recommendations()
    return booksBatch

@app.get('/books')
def get_books_from_db():
    books=get_all_books()
    return books


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("server:app", host="0.0.0.0", port=port)


