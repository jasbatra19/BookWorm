class BooksJson:
    def __init__(self, books_list):
        self.books = [self._transform_book(book) for book in books_list]
    
    def _transform_book(self, book_dict):
        volume_info = book_dict.get('volumeInfo', {})
        return {
            'title': volume_info.get('title'),
            'author': volume_info.get('authors', [])[0] if volume_info.get('authors') else "Unknown",  # Taking first author
            'description': volume_info.get('description', 'No description available'),
            'publishedDate': volume_info.get('publishedDate', 'N/A'),
            'pageCount': volume_info.get('pageCount', 0),
            'averageRating': volume_info.get('averageRating', 0),
            'ratingsCount': volume_info.get('ratingsCount', 0),
            'categories': volume_info.get('categories', []),
            'thumbnail': volume_info.get('imageLinks', {}).get('thumbnail', 'No image available'),
            'maturityRating': volume_info.get('maturityRating', 'N/A'),
        }

    def get_books(self):
        return self.books
