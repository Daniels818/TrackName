import re


def clean_query(text):
    """Normalize the user's search query before sending it to the Genius API."""
    text = text.lower()
    text = re.sub(r'[.,;:!?"()\[\]{}]', "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()
