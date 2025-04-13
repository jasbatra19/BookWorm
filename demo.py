from fastapi import FastAPI,Query
from fastapi.staticfiles import StaticFiles
from src.api.get_api import HelloBookWorms
from typing import Optional

app= FastAPI()
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

@app.get('/mostRead/{top}')
def get_bestSellers(top:int):
    return client.get_bestsellers(limit=top)

@app.get('/newReleases')
def get_bestSellers(top:int,year:Optional[int],month:Optional[int]):
    return client.get_new_releases_by_year_or_month(limit=top,year=year,month=month)


