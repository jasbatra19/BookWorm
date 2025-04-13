# https://www.googleapis.com/books/v1/volumes?q=fiction&maxResults=5&key=YOUR_API_KEY

import abc
from src.plugins.responseJson import BooksJson
class GetBooksInfo(abc.ABC):
    def get_bestsellers()->BooksJson:
        '''gets bestseller books according to goodread'''
        pass

    def get_author(self,author_name)->BooksJson:
        '''gets books by author name.'''
        pass

    def get_by_title(self,title_name)->BooksJson:
        '''gets books by title.'''
        pass

    def get_reviews()->BooksJson:
        '''gets reviews'''
        pass

    def get_genre()->BooksJson:
        '''gets books by genre'''
        pass

