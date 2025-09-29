from fastapi import FastAPI,Query
import uvicorn
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from src.api.get_api import HelloBookWorms
from typing import Optional
from datetime import datetime
from src.database.db_conn import *
import os



app = FastAPI(
    title="BookWorm API",
    description="API for discovering books through Reddit discussions and Google Books",
    version="1.0.0"
)


origins = [
    "http://localhost:3000",  # React app running here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],      # or restrict to ["GET", "POST"] etc.
    allow_headers=["*"],      # or restrict to specific headers
)


client=HelloBookWorms()


@app.get('/')
def root():
    return {"message":"API is running fine. :)", "status":"200"}

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

    

@app.get('/recommendationsreddit')
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


