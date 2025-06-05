class BooksJson:
    def __init__(self, books_list):
        self.books = [self._transform_book(book) for book in books_list]
    
    def _transform_book(self, book_dict):
        volume_info = book_dict.get('volumeInfo', {})
        authors = volume_info.get('authors')
        return {
            'bookId': book_dict.get('id', 'N/A'),
            'title': volume_info.get('title', 'Untitled'),
            'author': authors[0] if authors else 'Unknown',
            'description': volume_info.get('description', 'No description available'),
            'publishedDate': volume_info.get('publishedDate', 'N/A'),
            'pageCount': volume_info.get('pageCount', 0),
            'averageRating': volume_info.get('averageRating', 0),
            'ratingsCount': volume_info.get('ratingsCount', 0),
            'categories': volume_info.get('categories', []),
            'thumbnail': volume_info.get('imageLinks', {}).get('thumbnail', 'No image available'),
            'maturityRating': volume_info.get('maturityRating', 'N/A'),
            'previewLink': volume_info.get('previewLink', ''),
        }

    def get_books(self):
        return self.books
