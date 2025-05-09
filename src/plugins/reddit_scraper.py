from src.plugins.reddit import RedditClient
from textblob import TextBlob
import spacy
import json
from src.plugins.spacy_reddit import extract_books,clean_book_titles


def get_reddit_recommendations():
    reddit=RedditClient()
    subreddit = reddit.get_subreddit('suggestmeabook')  
    top_posts = subreddit.search("recommended",sort='relevance',time_filter='month',limit=10)
    all_posts=[]
    for post in top_posts:
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
    # nlp = spacy.load("en_core_web_sm")
    # doc = nlp(post.selftext)

    # for ent in doc.ents:
    #     if ent.label_ == "WORK_OF_ART":
    #         print("Book title maybe? 📖", ent.text)

    # sentiment = TextBlob(post.selftext).sentiment.polarity
    # if sentiment > 0:
    #     print("Positive Post 🎉")
    # elif sentiment < 0:
    #     print("Negative Post 😒")
    # else:
    #     print("Neutral 😐")


# post = reddit.submission(id="1jwm6vh")  # April 11, 2025 Weekly Thread

# post.comments.replace_more(limit=None)  # Load all comments

# for top_level_comment in post.comments:
#     print("🔎 Request:", top_level_comment.body[:200])  # Trimmed preview
#     for reply in top_level_comment.replies:
#         print("📚 Suggestion:", reply.body[:200])  # Each suggestion
#         print("-" * 40)
