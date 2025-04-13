import requests
from bs4 import BeautifulSoup
from fastapi.responses import JSONResponse

def best_selling_books(type,limit=10,meta_data={}):
    url_map={
        1:f'https://www.goodreads.com/book/popular_by_date/{meta_data.get('year')}/{meta_data.get('month')}',
        2:f'https://www.goodreads.com/book/most_read'
    }
    url=url_map.get(type)
    print(url)
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    book_rows = soup.select("tr[itemtype='http://schema.org/Book']")[:limit]
    
    books=[]
    for row in book_rows:
        title_tag = row.select_one("a.bookTitle span")
        author_tag = row.select_one("a.authorName span")
        cover_tag = row.select_one("img.bookCover")

        books.append({
            "title": title_tag.text.strip() if title_tag else "N/A",
            "author": author_tag.text.strip() if author_tag else "N/A",
            "cover_image": cover_tag['src'] if cover_tag else None
        })
    print(books)
    book=JSONResponse(content={"books": books})
    print(book)
    return book

