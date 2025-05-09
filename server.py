from fastapi import FastAPI,Query
from fastapi.staticfiles import StaticFiles
from src.api.get_api import HelloBookWorms
from typing import Optional
from datetime import datetime
from src.plugins.reddit_scraper import get_reddit_recommendations
from src.database.bookStore import create_table,connect_db,insert_book,get_all_books,get_book_by_name

app= FastAPI()
create_table()
app.mount("/static", StaticFiles(directory="static", html=True), name="static")
client=HelloBookWorms()

@app.get('/author/{author_name}')
def get_author(author_name:str):
    return client.get_author(author_name=author_name)
    
@app.get('/title/{title}')
def get_by_title(title:str):
    return client.get_by_title(title_name=title)

@app.get('/genre/{genre}')
def get_by_genre(genre:str):
    return client.get_genre(genre=genre)

@app.get('/bestseller/{top}')
async def get_bestSellers(top:int):
    return await client.get_bestsellers(limit=top)

@app.get('/newReleases')
def get_bestSellers(top: Optional[int] = 10, year: Optional[int] = None, month: Optional[int] = None):
    year = year if year is not None else datetime.now().year
    month = month if month is not None else datetime.now().month
    return client.get_new_releases_by_year_or_month(limit=top, year=year, month=month)

@app.get('/reddit_recommendations')
def reddit_recommendation():
    recommendations=[]
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



