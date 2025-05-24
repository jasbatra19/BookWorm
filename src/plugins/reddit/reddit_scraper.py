from src.plugins.reddit.redditClient import RedditClient
from textblob import TextBlob
import spacy
import json
from src.plugins.reddit.tags import tags,search_criteria
from src.plugins.reddit.preprocessing import extract_books,clean_book_titles


MIN_SCORE = 10
def get_reddit_recommendations():
    reddit=RedditClient()
    subreddit = reddit.get_subreddit(tags)  
    top_posts = subreddit.search(search_criteria,sort='hot',time_filter='day',limit=10)
    all_posts=[]
    visited_posts_id=[] 
    for post in top_posts:
        if(post.id in visited_posts_id or post.score < 10):
            continue
        post_data = {
            "id": post.id,
            "title": post.title,
            "score": post.score,
            "num_comments": post.num_comments,
            "link": f"https://www.reddit.com{post.permalink}",
            "content": post.selftext,
            "comments": [comment.body for comment in post.comments if hasattr(comment, "body")]
        }
        
        all_posts.append(post_data)

    # Save to a JSON file
    with open("reddit_posts.json", "w", encoding="utf-8") as f:
        json.dump(all_posts, f, ensure_ascii=False, indent=4)

    with open("reddit_posts.json", "r", encoding="utf-8") as f:
        jsonData=json.load(f)

    books=extract_books(jsonData)
    preprocessed_books=clean_book_titles(books)
    print(preprocessed_books[0:50])
    # most occurring ones return
    return preprocessed_books[0:50]

get_reddit_recommendations()
