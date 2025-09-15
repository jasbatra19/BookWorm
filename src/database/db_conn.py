import os
from dotenv import load_dotenv
from supabase import create_client, Client
from typing import List, Dict, Any, Optional

load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")

if not url or not key:
    raise ValueError("Missing SUPABASE_URL or SUPABASE_KEY in environment variables")

supabase: Client = create_client(url, key)

# Table creation is done via Supabase dashboard or SQL editor
# You'll need to create these tables manually in Supabase:

"""
CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    bookId TEXT UNIQUE,
    title TEXT,
    author TEXT,
    description TEXT,
    publishedDate TEXT,
    pageCount INTEGER,
    averageRating REAL,
    ratingsCount INTEGER,
    categories TEXT,
    thumbnail TEXT,
    maturityRating TEXT,
    recommendedPercentage INTEGER DEFAULT 0,
    dateOfProcessing TIMESTAMP DEFAULT NOW()
);

CREATE TABLE booksId (
    id SERIAL PRIMARY KEY,
    postId TEXT UNIQUE,
    title TEXT,
    link TEXT,
    score INTEGER,
    num_comments INTEGER,
    content TEXT,
    comments TEXT
);

CREATE TABLE book_post_map (
    id SERIAL PRIMARY KEY,
    book_id INTEGER REFERENCES books(id),
    post_id INTEGER REFERENCES booksId(id),
    UNIQUE(book_id, post_id)
);
"""

def existing_ids(post_id: str) -> bool:
    """Check if the current post is already in DB"""
    try:
        response = supabase.table("booksId").select("*").eq("postId", post_id).execute()
        if response.data:
            print('Post already exists in the database.')
            return True
        return False
    except Exception as e:
        print(f"Error checking existing post: {e}")
        return False

def post_info(post_data: Dict[str, Any]) -> bool:
    """Stores post information in booksId table"""
    try:
        data = {
            "postId": post_data["id"],
            "title": post_data["title"],
            "link": post_data["link"],
            "score": post_data["score"],
            "num_comments": post_data["num_comments"],
            "content": post_data["content"],
            "comments": str(post_data["comments"])
        }
        
        response = supabase.table("booksId").insert(data).execute()
        if response.data:
            print("Post inserted successfully")
            return True
        return False
    except Exception as e:
        print(f"Error inserting post: {e}")
        return False

def insert_book(book: Dict[str, Any]) -> bool:
    """Insert book into books table"""
    try:
        data = {
            "bookId": book['bookId'],
            "title": book['title'],
            "author": book['author'],
            "description": book['description'],
            "publishedDate": book['publishedDate'],
            "pageCount": book['pageCount'],
            "averageRating": book['averageRating'],
            "ratingsCount": book['ratingsCount'],
            "categories": ', '.join(book['categories']) if isinstance(book['categories'], list) else book['categories'],
            "thumbnail": book['thumbnail'],
            "maturityRating": book['maturityRating']
        }
        
        response = supabase.table("books").insert(data).execute()
        if response.data:
            print('Book inserted into the database')
            return True
        return False
    except Exception as e:
        print(f"Error inserting book: {e}")
        return False

def get_all_books() -> List[Dict[str, Any]]:
    """Fetches all the books in the books db"""
    try:
        response = supabase.table("books").select("*").execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Error fetching all books: {e}")
        return []

def get_book_by_ID(book_id: str) -> List[Dict[str, Any]]:
    """Get book by bookId"""
    try:
        response = supabase.table("books").select("*").eq("bookId", book_id).execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Error fetching book by ID: {e}")
        return []

def get_book_by_name(book_title: str) -> List[Dict[str, Any]]:
    """Fetches books by title"""
    try:
        response = supabase.table("books").select("*").eq("title", book_title).execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Error fetching book by name: {e}")
        return []

def updateBooksRecommendedPercentage(book_id: str) -> int:
    """Update recommendations if the book is present in some other post as well"""
    try:
        # First get current recommendedPercentage
        current_response = supabase.table("books").select("recommendedPercentage").eq("bookId", book_id).execute()
        
        if current_response.data:
            current_percentage = current_response.data[0].get("recommendedPercentage", 0) or 0
            new_percentage = current_percentage + 1
            
            # Update the record
            response = supabase.table("books").update({
                "recommendedPercentage": new_percentage,
                "dateOfProcessing": "NOW()"
            }).eq("bookId", book_id).execute()
            
            if response.data:
                print('Book already exists in the database. recommendedPercentage updated')
                return len(response.data)  # Number of rows updated
        
        return 0
    except Exception as e:
        print(f"Error updating recommendation percentage: {e}")
        return 0

def map_book_to_post(book_id: int, post_id: int) -> bool:
    """Create mapping between book and post"""
    try:
        data = {
            "book_id": book_id,
            "post_id": post_id
        }
        
        # Use upsert to handle duplicates gracefully
        response = supabase.table("book_post_map").upsert(data).execute()
        return bool(response.data)
    except Exception as e:
        print(f"Error mapping book to post: {e}")
        return False

def get_books_from_post(post_id: int) -> List[Dict[str, Any]]:
    """Get all books associated with a post"""
    try:
        response = supabase.table("books").select("""
            *,
            book_post_map!inner(post_id)
        """).eq("book_post_map.post_id", post_id).execute()
        
        return response.data if response.data else []
    except Exception as e:
        print(f"Error fetching books from post: {e}")
        return []

def get_posts_from_book(book_id: int) -> List[Dict[str, Any]]:
    """Get all posts associated with a book"""
    try:
        response = supabase.table("booksId").select("""
            *,
            book_post_map!inner(book_id)
        """).eq("book_post_map.book_id", book_id).execute()
        
        return response.data if response.data else []
    except Exception as e:
        print(f"Error fetching posts from book: {e}")
        return []

# Helper function to get internal IDs (since Supabase uses auto-incrementing IDs)
def get_book_internal_id(book_id: str) -> Optional[int]:
    """Get the internal database ID for a book by bookId"""
    try:
        response = supabase.table("books").select("id").eq("bookId", book_id).execute()
        if response.data:
            return response.data[0]["id"]
        return None
    except Exception as e:
        print(f"Error getting book internal ID: {e}")
        return None

def get_post_internal_id(post_id: str) -> Optional[int]:
    """Get the internal database ID for a post by postId"""
    try:
        response = supabase.table("booksId").select("id").eq("postId", post_id).execute()
        if response.data:
            return response.data[0]["id"]
        return None
    except Exception as e:
        print(f"Error getting post internal ID: {e}")
        return None