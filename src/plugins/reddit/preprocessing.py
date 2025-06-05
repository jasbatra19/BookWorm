import spacy
import re
import json

nlp = spacy.load("en_core_web_sm") 
def extract_books(Collection):
    books=[]
    for data in Collection:
        # content 
        doc = nlp(data['content'])
        book_titles = [ent.text for ent in doc.ents if ent.label_ == "WORK_OF_ART"]
        if(book_titles):
            books.append(book_titles)
        book_titles = re.findall(r'\b([A-Za-z0-9\s\'\":\-&]+)\sby\s[A-Z][a-zA-Z]+(?:\s[A-Z][a-zA-Z]+)?', data['content'])
        if(book_titles):
            books.append(book_titles)
        
        # comments
        for comment in data['comments']:
            doc=nlp(comment)
            book_titles = [ent.text for ent in doc.ents if ent.label_ == "WORK_OF_ART"]
            if(book_titles and len(book_titles)>10):
                books.append(book_titles)
            book_titles = re.findall(r'\b([A-Za-z0-9\s\'\":\-&]+)\sby\s[A-Z][a-zA-Z]+(?:\s[A-Z][a-zA-Z]+)?', comment)
            if(book_titles):
                books.append(book_titles)
            
    with open("extracted_books_content.json", "w", encoding="utf-8") as f:
            json.dump((books), f, ensure_ascii=False, indent=4)
    with open("extracted_books_comments.json", "w", encoding="utf-8") as f:
                json.dump(books, f, ensure_ascii=False, indent=4)
    return books

def clean_book_titles(nested_list):
    cleaned_books = set()
    split_pattern = r'\n+|,|and|by|- |–|•|\||\. '
    for sublist in nested_list:
        for raw_entry in sublist:
            parts = re.split(split_pattern, raw_entry)
            for part in parts:
                title = part.strip().title()
                if len(title) > 2 and not title.lower().startswith("i am") and not title.lower().startswith("nan"):
                    cleaned_books.add(title)
    with open("reddit_books.json", "w", encoding="utf-8") as f:
        json.dump(list(set(cleaned_books)), f, ensure_ascii=False, indent=4)

    return sorted(cleaned_books)





