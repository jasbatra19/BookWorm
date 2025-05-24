from fastapi import FastAPI,Query
from fastapi.middleware.cors import CORSMiddleware
from src.api.get_api import HelloBookWorms
from typing import Optional
from datetime import datetime
from src.plugins.reddit.reddit_scraper import get_reddit_recommendations
from src.database.bookStore import create_table,connect_db,insert_book,get_all_books,get_book_by_name

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
create_table()
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
def reddit_recommendation():
    recommendations=[]
    print('getting reddit recommended book')
    books=get_reddit_recommendations()
    for book in books:
        result=get_book_by_name(book)
        print(f"result by sql: {result}")
        if(result):
            recommendations.append(result)
        else:
            result=get_by_title(book)
            recommendations.append(result)
            insert_book(result[0])

    return recommendations

@app.get('/getAllBooks')
def get_books_from_db():
    books=get_all_books()
    return books



