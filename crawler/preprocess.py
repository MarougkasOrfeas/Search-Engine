import datetime
import unicodedata
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re


def preprocess_abstract(text):
    """
    Preprocesses the abstract text of an academic paper.

    Parameters:
    - text (str): The raw abstract text.

    Returns:
    - str: The preprocessed abstract text.
    """
    tokens = word_tokenize(text)  # Τokenization
    tokens = [re.sub(r'[^a-zA-Z0-9]', '', unicodedata.normalize('NFKD', token.lower())) for token in tokens]
    stop_words = set(stopwords.words('english'))  # stop-word removal
    tokens = [token for token in tokens if token not in stop_words]
    lemmatizer = WordNetLemmatizer()  # lemmatization
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    preprocessed_text = ' '.join(tokens)
    return preprocessed_text


def preprocess_authors(authors_text):
    """
    Preprocesses the authors' names from the raw text.

    Parameters:
    - authors_text (str): The raw authors' names text.

    Returns:
    - str: The preprocessed authors' names.
    """
    # Remove the word "Authors" and other unnecessary characters
    authors_text = re.sub(r'Authors:|\\n\s*', ' ', authors_text, flags=re.IGNORECASE).strip()

    # Extract individual author names
    authors_list = re.split(r'\\n\\n|,', authors_text)

    # Remove extra spaces and handle names without clear separation
    joined_authors = []
    for name in authors_list:
        # Remove capital letter followed by a dot (initials)
        name = re.sub(r'\b[A-Z]\.\b', '', name)
        name_parts = name.strip().split()
        joined_name = ''.join(name_parts)
        joined_authors.append(joined_name)

    # Concatenate the joined authors into a single string
    preprocessed_authors = ' '.join(joined_authors)
    preprocessed_authors = preprocessed_authors.lower()

    return preprocessed_authors


def preprocess_date(date_text):
    """
    Preprocesses the date string from the raw text.

    Parameters:
    - date_text (str): The raw date string.

    Returns:
    - str or None: The preprocessed date string or None if the format is invalid.
    """
    # Extract day, month, and year from the date string
    match = re.search(r'(\d+)\s*([a-zA-Z]+)\s*,\s*(\d+)', date_text)
    if match:
        day, month, year = match.groups()
        # Convert month name to its numeric representation
        month = datetime.datetime.strptime(month, '%B').strftime('%B')
        # Concatenate day, month, and year in the desired format
        preprocessed_date = f"{day}{month}{year}"
        preprocessed_date = preprocessed_date.lower()
        return preprocessed_date
    else:
        return None  # Return None for invalid date format


def preprocess_title(title_text):
    """
    Preprocesses the title of an academic paper.

    Parameters:
    - title_text (str): The raw title text.

    Returns:
    - str: The preprocessed title text.
    """
    # Remove special characters and normalize to lowercase
    preprocessed_title = re.sub(r'[^a-zA-Z0-9\s]', '', unicodedata.normalize('NFKD', title_text.lower()))
    # Tokenization: Split the text into words
    tokens = word_tokenize(preprocessed_title)
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    # Lemmatization: Convert words to their base form
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    # Join the tokens back into a preprocessed title
    preprocessed_title = ' '.join(tokens)
    return preprocessed_title
