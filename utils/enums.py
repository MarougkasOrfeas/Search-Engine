from enum import Enum


class Paths(Enum):
    # LOG path
    LOGS_APP_PATH = 'logs/app.log'

    # JSON files path
    PAPERS_PATH = 'data/papers.json'
    PAPERS_PREPROCESSED_PATH = 'data/papers_preprocessed.json'
    INVERTED_INDEX_AUTHORS_PATH = 'data/inverted_index_authors.json'
    INVERTED_INDEX_ABSTRACT_PATH = 'data/inverted_index_abstract.json'
    INVERTED_INDEX_DATE_PATH = 'data/inverted_index_date.json'
    INVERTED_INDEX_TITLE_PATH = 'data/inverted_index_title.json'


class ArxivConfig(Enum):
    BASE_URL = "https://arxiv.org/search/"
    DEFAULT_VALUE = 100
    QUERY = 'python'
