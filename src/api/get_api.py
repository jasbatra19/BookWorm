from src.wrapper.get import GetBooksInfo
import requests
from src.plugins.reddit.scraper import best_selling_books
from src.plugins.responseJson import BooksJson
from datetime import datetime
import httpx, asyncio
import json
class HelloBookWorms(GetBooksInfo):
    def __init__(self):
        self.baseurl='https://www.googleapis.com'
        self.url=''
        print('initializing the book api')
        return 
    
    async def get_bestsellers(self,genre='fiction',limit=100)->BooksJson:
        print(f'getting top {limit} best selling books')
        response=best_selling_books(baseURL=self.baseurl,urlType=1,genre=genre,limit=limit)
        print(f'fetched top {limit} best selling books')
        print("response",response)
        return response

    def get_new_releases_by_year_or_month(self,year=datetime.now().year,month=datetime.now().month,limit=100)->BooksJson:
        print(f'getting new release as per {year} and {month}')
        response=best_selling_books(baseURL=self.baseurl,urlType=2,limit=limit,metadata={'year':year,'month':month})
        print(f'Books fetched')
        return response
        
    def get_by_title(self,title_name)->BooksJson:
        print(self.url)
        self.url=self.baseurl+f'/books/v1/volumes?q=intitle:"{title_name}"'
        print(self.url)
        response= requests.get(self.url).json()
        print(f'book fetched with title name {title_name}')
        return BooksJson(response['items']).get_books()

    def get_author(self,author_name)->BooksJson:
        print(self.url)
        self.url=self.baseurl+f'/books/v1/volumes?q=inauthor:"{author_name}"'
        print(self.url)
        response= requests.get(self.url).json()
        print(f'book fetched with author name {author_name}')
        return BooksJson(response['items']).get_books()

    def get_genre(self,genre)->BooksJson:
        print(self.url)
        self.url=self.baseurl+f'/books/v1/volumes?q=subject:"{genre}"'
        print(self.url)
        response= requests.get(self.url).json()
        print(f'book fetched with {genre}')
        return BooksJson(response['items']).get_books()
        
    def get_reviews()->BooksJson:
        pass

    def reddit()->BooksJson:
        pass

    async def fetch_book_data(self, title: str, client: httpx.AsyncClient):
        try:
            self.url=self.baseurl+f'/books/v1/volumes?q=intitle:{title}'
            print(self.url)
            res= await client.get(self.url)
            res.raise_for_status()
            books = BooksJson(res.json().get("items", [])).get_books()
            with open("results_fecth.json", "w", encoding="utf-8") as f:
                json.dump(books, f, ensure_ascii=False, indent=4)
            return books[0] if books else None
        except Exception as e:
            print(f"Failed to fetch {title}: {e}")
            return None


    async def batch_fetch_books(self, titles: list[str]):
        async with httpx.AsyncClient() as client:
            tasks = [self.fetch_book_data(t, client) for t in titles]
            results = await asyncio.gather(*tasks)
            with open("results.json", "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=4)
        return results


        
        