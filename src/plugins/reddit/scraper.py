import requests
from bs4 import BeautifulSoup
from fastapi.responses import JSONResponse
from datetime import datetime
from src.plugins.responseJson import BooksJson

def best_selling_books(urlType=int,baseURL='',genre='fiction',limit=10000,metadata={}):
    print("URLTYPE",urlType)
    url_map={
        1:f'/books/v1/volumes?q=subject:"{genre}"&orderBy=relevance&maxResult={limit}',
        2:f'/books/v1/volumes?q=subject:"{genre}"&orderBy=newest&maxResult={limit}'
    }
    URL=baseURL+url_map.get(urlType,url_map[2])
    print(URL)
    response=requests.get(url=URL).json()
    books_response=BooksJson(response['items']).get_books()
    books=[]
    for item in books_response:
        if(urlType==1):
            if(item.get('averageRating',0)>3):
                books.append(item)

        elif urlType == 2:
            if item.get('publishedDate'):
                published_date = item.get('publishedDate')
                try:
                    if len(published_date) == 4:  # If only year is provided, format it as "YYYY-01-01"
                        published_date = published_date + "-01-01"
                    # Convert publishedDate to datetime object
                    published_date_obj = datetime.strptime(published_date, "%Y-%m-%d")
                    if published_date_obj.year == datetime.now().year:
                        books.append(item)
                except ValueError:
                    # Handle cases where the publishedDate is not in expected format
                    print(f"Invalid date format for book: {item.get('title')}")
                    continue

    return books


