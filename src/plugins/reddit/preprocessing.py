import spacy
import re
import json

with open("reddit_posts.json", "r", encoding="utf-8") as f:
    jsonData=json.load(f)


def extract_books(Collection):
    books=[]
    nlp = spacy.load("en_core_web_sm") 
    for data in Collection:
        # content 
        doc = nlp(data['content'])
        book_titles = [ent.text for ent in doc.ents if ent.label_ == "WORK_OF_ART"]
        if(book_titles):
            books.append(book_titles)
        book_titles = re.findall(r'([A-Za-z\s]+)\sby\s[A-Za-z\s]+', data['content'])
        if(book_titles):
            books.append(book_titles)
        
        # comments
        for comment in data['comments']:
            doc=nlp(comment)
            book_titles = [ent.text for ent in doc.ents if ent.label_ == "WORK_OF_ART"]
            if(book_titles and len(book_titles)>10):
                books.append(book_titles)
            book_titles = re.findall(r'([A-Za-z\s]+)\sby\s[A-Za-z\s]+', comment)
            if(book_titles):
                books.append(book_titles)
            
    with open("extracted_books_content.json", "w", encoding="utf-8") as f:
            json.dump((books), f, ensure_ascii=False, indent=4)
    with open("extracted_books_comments.json", "w", encoding="utf-8") as f:
                json.dump(books, f, ensure_ascii=False, indent=4)
    return books

def clean_book_titles(nested_list):
    cleaned_books = []
    # skip_keywords = ['nothing', 'i have read', 'love', 'one']
    split_pattern = r'\n+|,|and|by|- |–|•|\||\. '
    for sublist in nested_list:
        for raw_entry in sublist:
            # print(raw_entry)
            # if any(skip.lower() in raw_entry.lower() for skip in skip_keywords):
            #     continue

            parts = re.split(split_pattern, raw_entry)

            for part in parts:
                title = part.strip().title()
                if len(title) > 2 and not title.lower().startswith("i am") and not title.lower().startswith("nan"):
                    cleaned_books.append(title)
    with open("reddit_books.json", "w", encoding="utf-8") as f:
        json.dump(list(set(cleaned_books)), f, ensure_ascii=False, indent=4)

    return list(set(cleaned_books))





