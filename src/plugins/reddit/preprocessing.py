import spacy
import re
import json

def get_nlp():
    if not hasattr(get_nlp, "nlp"):
        get_nlp.nlp = spacy.load("en_core_web_trf")
    return get_nlp.nlp


# Improved book regex pattern

def extract_book_titles(text_list):
    """Extract book titles from a list of text strings."""
    titles = []
    skip_keywords = [
        'what', 'how', 'why', 'where', 'who', 'when', 'do you', 
        'thoughts on', 'any favorite', 'theory time', 'if there is',
        'should', 'would you', 'could you', 'significance of',
        'realization does', 'role does', 'situation that','spoiler','spoilers','read','reading','recommend','recommendation','discuss'
    ]
    for text in text_list:
        # Skip empty, deleted, or clearly non-book entries
        if not text or not isinstance(text, str):
            continue

        if not text or text.strip() in ['[deleted]', ''] or 'wanna do this' in text.lower():
            continue
        
        if text.endswith('?'):
            continue
        
        text_lower = text.lower()
        question_count = sum(1 for kw in ['what', 'how', 'why', 'does', 'do you'] if kw in text_lower)
        if question_count >= 2:
            continue

        if any(text_lower.startswith(kw) for kw in skip_keywords):
            continue

        # Pattern 1: Text between asterisks (markdown bold/italic)
        asterisk_match = re.search(r'\*([^*]+)\*', text)
        if asterisk_match:
            title = asterisk_match.group(1).strip()
            if len(title) > 1:  # Avoid single characters
                titles.append(title)
            continue
        
        # Pattern 2: "Title by Author" format
        by_pattern = re.search(r'^([^.,:\n]+?)\s+by\s+[A-Z][a-z]+', text)
        if by_pattern:
            title = by_pattern.group(1).strip()
            # Remove leading articles or phrases
            # title = re.sub(r'^(I read |An old one:\s*)', '', title, flags=re.IGNORECASE)
            if len(title) > 1:  # Avoid single characters
                titles.append(title)
            continue
        
        # Pattern 3: "Author: Title" format
        author_colon = re.search(r'^[A-Z][a-z]+\s+[A-Z][a-z]+:\s+(.+?)(?:\s+by|\.|$)', text)
        if author_colon:
            title = author_colon.group(1).strip()
            if len(title) > 1:  # Avoid single characters
                titles.append(title)
            continue
        
        # Pattern 4: "Title, by Author" format
        comma_by = re.search(r'^(.+?),\s+by\s+[A-Z]', text)
        if comma_by:
            title = comma_by.group(1).strip()
            if len(title) > 1:  # Avoid single characters
                titles.append(title)
            continue
        
        # Pattern 5: Multiple titles in one entry (separated by \n\n)
        if '\n\n' in text:
            parts = text.split('\n\n')
            for part in parts:
                part_match = re.search(r'^([^.,\n]+?)\s+by\s+', part)
                if part_match:
                    if len(title) > 1:  # Avoid single characters
                        titles.append(part_match.group(1).strip())
            if titles and titles[-1] != text:  # If we found something
                continue
        
        # Pattern 6: Title at start before period or context words
        simple_match = re.search(r'^([A-Z][^.,\n]+?)(?:\s+by|\.|$)', text)
        if simple_match and not any(word in text.lower()[:30] for word in ['could you', 'i did', 'i ran', 'this is']):
            title = simple_match.group(1).strip()
            # Additional cleanup
            title = re.sub(r'\s+\([^)]+\)$', '', title)  # Remove trailing parentheses
            if len(title) > 1:  # Avoid single letters
                titles.append(title)

    # avoiding duplicates
    seen = set()
    unique_titles = []
    for title in titles:
        title_normalized = title.lower().strip('.,')
        if title_normalized not in seen:
            seen.add(title_normalized)
            unique_titles.append(title)
    return unique_titles

def extract(Collection):
    all_text = []
    
    for data in Collection:
        # Extend (not append) to flatten the lists
        if 'content' in data and data['content']:
            all_text.extend(data['content'])
        if 'comments' in data and data['comments']:
            all_text.extend(data['comments'])
    
    titles = extract_book_titles(all_text)
    return titles


book_by_author_pattern = r'(?:["“\']?\*?)([A-Z][\w\s:\-,&]{3,})\s+by\s+([A-Z][a-zA-Z\.\'\-]+(?:\s+[A-Z][a-zA-Z\.\'\-]+)*)(?:\*?["”\']?)'
def extract_books(Collection):
    content_books = []
    comment_books = []

    for data in Collection:
        nlp = get_nlp()
        # --- Content ---
        doc = nlp(data['content'])
        ner_titles = [ent.text for ent in doc.ents if ent.label_ == "WORK_OF_ART"]
        if ner_titles:
            content_books.append(ner_titles)
        with open("extracts/ner_titles_content.json", "a", encoding="utf-8") as f:
            json.dump(ner_titles, f, ensure_ascii=False, indent=4)

        regex_titles = re.findall(book_by_author_pattern, data['content'])
        if regex_titles:
            content_books.append([' '.join(match) for match in regex_titles])
        with open("extracts/regex_titles_content.json", "a", encoding="utf-8") as f:
            json.dump(regex_titles, f, ensure_ascii=False, indent=4)

        # --- Comments ---
        for comment in data['comments']:
            doc = nlp(comment)
            ner_titles = [ent.text for ent in doc.ents if ent.label_ == "WORK_OF_ART"]
            if ner_titles:
                comment_books.append(ner_titles)
            with open("extracts/ner_titles_comment.json", "a", encoding="utf-8") as f:
                json.dump(ner_titles, f, ensure_ascii=False, indent=4)

            regex_titles = re.findall(book_by_author_pattern, comment)
            if regex_titles:
                comment_books.append([' '.join(match) for match in regex_titles])
            with open("extracts/regex_titles_comment.json", "a", encoding="utf-8") as f:
                json.dump(regex_titles, f, ensure_ascii=False, indent=4)

    with open("extracts/extracted_books_content.json", "w", encoding="utf-8") as f:
        json.dump(content_books, f, ensure_ascii=False, indent=4)

    with open("extracts/extracted_books_comments.json", "w", encoding="utf-8") as f:
        json.dump(comment_books, f, ensure_ascii=False, indent=4)

    return content_books + comment_books


def clean_book_titles(nested_list):
    cleaned_books = set()
    split_pattern = r'\\+|,|and|- |–|•|\||\.|\\n\\n|\\n'
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

    with open("extracts/reddit_books.json", "w", encoding="utf-8") as f:
        json.dump(sorted(cleaned_books), f, ensure_ascii=False, indent=4)

    return sorted(cleaned_books)