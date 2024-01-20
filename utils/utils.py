import logging
from datetime import datetime


def inverted_index_search(query, inverted_index):
    """
    Search for a query in the inverted index.

    Parameters:
    - query (str): The search query.
    - inverted_index (dict): The inverted index to search in.

    Returns:
    - list: List of document IDs that match the query.
    """
    query = query.lower().replace(" ", "")
    matching_documents = inverted_index.get(query, {}).get('documents', [])
    logging.debug(f"Inverted Index Search - Query: {query}, Matching Documents: {matching_documents}")
    return matching_documents


def sort_results(papers_to_display, sort_by):
    """
    Sorts the papers based on the specified sorting option.

    Parameters:
    - papers_to_display: List of dictionaries representing papers.
    - sort_by: Sorting option ('date', 'author', 'title').

    Returns:
    - Sorted list of papers.
    """
    if sort_by == 'date':
        logging.info("Sorting results by date.")
        return sorted(papers_to_display, key=lambda x: parse_date(x.get('Date', '')), reverse=True)
    elif sort_by == 'author':
        logging.info("Sorting results by author.")
        return sorted(papers_to_display, key=lambda x: x.get('Authors', ''))
    elif sort_by == 'title':
        logging.info("Sorting results by title.")
        return sorted(papers_to_display, key=lambda x: x.get('Title', ''))
    else:
        return papers_to_display  # No sorting, return as is


def parse_date(date_string):
    """
    Parse the date string into a datetime object.

    Parameters:
    - date_string: Date string in a specific format.

    Returns:
    - Parsed datetime object.
    """
    try:
        # Extract the date part from the string (ignoring additional information)
        date_part = date_string.split(';')[0].strip()
        # Parse the date into a datetime object
        return datetime.strptime(date_part, "Submitted %d %B, %Y")
    except ValueError:
        # Handle the case where parsing fails
        return datetime.min


# Function to read the last N lines from a file
def read_last_n_lines(file_path, n):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            return lines[-n:]
    except FileNotFoundError:
        return []
