import requests
import logging
from bs4 import BeautifulSoup

from exceptions.no_paper_exception import NoPapersFoundException
from utils.enums import Paths, ArxivConfig
from utils.json_config import json_write, json_read
from crawler.preprocess import preprocess_abstract, preprocess_authors, preprocess_date, preprocess_title
from crawler.inverted_index import create_and_save_inverted_index


def arxiv_crawler(query, max_results):
    """
    Perform crawling of arXiv papers based on the given query.

    Parameters:
    - query (str): The search query for arXiv papers.
    - max_results (int): The maximum number of results to fetch.
    """
    logging.info("Starting arXiv crawler...")
    base_url = ArxivConfig.BASE_URL.value

    params = {  # Parameters for the API request
        "query": query,
        "searchtype": "all",
        "abstracts": "show",
        "size": max_results,
        "order": "-submitted_date"
    }
    # Make the API request and parse the response with BeautifulSoup
    response = requests.get(base_url, params=params)
    soup = BeautifulSoup(response.text, "html.parser")
    # Extract relevant information from each paper
    papers = soup.find_all("li", class_="arxiv-result")

    if not papers:
        raise NoPapersFoundException("No papers found for the given query.")

    logging.info(f"Found {len(papers)} papers about {query}.")
    ID = 0
    # Lists to store raw and preprocessed data
    data_to_save = []
    data_preprocessed = []

    for paper in papers:
        title = paper.find("p", class_="title is-5 mathjax").text.strip()
        authors = paper.find("p", class_="authors").text.strip()
        abstract = paper.find("p", class_="abstract").text.strip()
        date = paper.find("p", class_="is-size-7").text.strip()
        # Preprocess the data
        preprocessed_abstract = preprocess_abstract(abstract)
        authors_processed = preprocess_authors(authors)
        date_processed = preprocess_date(date)
        title_processed = preprocess_title(title)
        ID += 1  # Increment ID for each paper
        paper_data = {  # Raw paper data
            "ID": ID,
            "Title": title,
            "Authors": authors,
            "Abstract": abstract,
            "Date": date,
        }
        data_to_save.append(paper_data)

        paper_data_processed = {  # Preprocessed paper data
            "ID": ID,
            "Title_processed": title_processed,
            "Authors_processed": authors_processed,
            "Abstract_processed": preprocessed_abstract,
            "Date_processed": date_processed,
        }
        data_preprocessed.append(paper_data_processed)
    # Save raw paper data to a JSON file
    json_write(data_to_save, Paths.PAPERS_PATH.value)
    logging.info(f"Processed those {len(data_to_save)} papers.")
    # Save preprocessed paper data to a JSON file
    json_write(data_preprocessed, Paths.PAPERS_PREPROCESSED_PATH.value)
    logging.info(f"Successfully saved all {len(data_preprocessed)} preprocessed papers to papers_preprocessed.json.")
    # Create and save inverted indices for preprocessed data
    data_preprocessed = json_read(Paths.PAPERS_PREPROCESSED_PATH.value)

    if data_preprocessed is not None:
        create_and_save_inverted_index(data_preprocessed, 'Authors_processed', Paths.INVERTED_INDEX_AUTHORS_PATH.value)
        create_and_save_inverted_index(data_preprocessed, 'Abstract_processed', Paths.INVERTED_INDEX_ABSTRACT_PATH.value)
        create_and_save_inverted_index(data_preprocessed, 'Date_processed', Paths.INVERTED_INDEX_DATE_PATH.value)
        create_and_save_inverted_index(data_preprocessed, 'Title_processed', Paths.INVERTED_INDEX_TITLE_PATH.value)

        logging.info("All Inverted indices created and saved.")
    else:
        logging.error("Failed to load preprocessed data. Inverted indices not created.")
