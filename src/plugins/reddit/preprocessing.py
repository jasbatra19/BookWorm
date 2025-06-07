import spacy
import re
import json

nlp = spacy.load("en_core_web_sm")

# Improved book regex pattern
book_by_author_pattern = r'(?:["“\']?\*?)([A-Z][\w\s:\-,&]{3,})\s+by\s+([A-Z][a-zA-Z\.\'\-]+(?:\s+[A-Z][a-zA-Z\.\'\-]+)*)(?:\*?["”\']?)'

def extract_books(Collection):
    content_books = []
    comment_books = []

    for data in Collection:
        # --- Content ---
        doc = nlp(data['content'])
        ner_titles = [ent.text for ent in doc.ents if ent.label_ == "WORK_OF_ART"]
        if ner_titles:
            content_books.append(ner_titles)

        regex_titles = re.findall(book_by_author_pattern, data['content'])
        if regex_titles:
            content_books.append([' '.join(match) for match in regex_titles])

        # --- Comments ---
        for comment in data['comments']:
            doc = nlp(comment)
            ner_titles = [ent.text for ent in doc.ents if ent.label_ == "WORK_OF_ART"]
            if ner_titles:
                comment_books.append(ner_titles)

            regex_titles = re.findall(book_by_author_pattern, comment)
            if regex_titles:
                comment_books.append([' '.join(match) for match in regex_titles])

    with open("extracted_books_content.json", "w", encoding="utf-8") as f:
        json.dump(content_books, f, ensure_ascii=False, indent=4)

    with open("extracted_books_comments.json", "w", encoding="utf-8") as f:
        json.dump(comment_books, f, ensure_ascii=False, indent=4)

    return content_books + comment_books


def clean_book_titles(nested_list):
    cleaned_books = set()
    split_pattern = r'\\n+|,|and|- |–|•|\||\.'
    common_single_words = {
        "About", "Both", "Explains", "It'S", "The", "And", "But", "Or", "If", "Is", "In", "Of", "To", "On", "At"
    }
    for sublist in nested_list:
        for raw_entry in sublist:
            parts = re.split(split_pattern, raw_entry)
            for part in parts:
                title = part.strip().title()
                if len(title) > 2 and not title.lower().startswith("i am") and not title.lower().startswith("nan"):
                    if not (len(title.split()) == 1 and title in common_single_words):
                        cleaned_books.add(title)

    with open("reddit_books.json", "w", encoding="utf-8") as f:
        json.dump(sorted(cleaned_books), f, ensure_ascii=False, indent=4)

    return sorted(cleaned_books)
