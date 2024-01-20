import logging

from flask import Flask, render_template, request

from crawler.web_crawler import arxiv_crawler
from exceptions.no_paper_exception import NoPapersFoundException
from utils.algorithms import boolean_search, vector_space_search, probabilistic_search, simple_search
from utils.json_config import load_data
from utils.enums import Paths, ArxivConfig
from utils.logging_config import configure_main_logging
from utils.utils import read_last_n_lines

app = Flask(__name__, template_folder='../templates')
configure_main_logging(Paths.LOGS_APP_PATH.value)


data_paths = {
    'author_data': Paths.INVERTED_INDEX_AUTHORS_PATH,
    'date_data': Paths.INVERTED_INDEX_DATE_PATH,
    'abstract_data': Paths.INVERTED_INDEX_ABSTRACT_PATH,
    'title_data': Paths.INVERTED_INDEX_TITLE_PATH,
    'paper_data': Paths.PAPERS_PATH,
    'paper_processed_data': Paths.PAPERS_PREPROCESSED_PATH,
}
data_sets = load_data(data_paths)


@app.route('/')
def index():
    logging.info('Accessed the index route.')
    return render_template('index.html')


@app.route('/crawl', methods=['POST'])
def crawl():
    query = request.form.get('crawl_query')
    max_results = int(request.form.get('max_results', ArxivConfig.DEFAULT_VALUE.value))
    try:
        logging.info(f"Received crawl request: {query}, max_results: {max_results}")
        arxiv_crawler(query=query, max_results=max_results)
        log_lines = read_last_n_lines(Paths.LOGS_APP_PATH.value, 15)
        return render_template('crawl_success.html', log_statements=log_lines)
    except NoPapersFoundException:
        error_message = "No papers found for the given query."
        return render_template('crawl_error.html', error_message=error_message)
    except Exception as e:
        logging.error(f"Crawling failed: {str(e)}")
        error_message = "An error occurred during crawling. Please try again later."
        return render_template('crawl_error.html', error_message=error_message)


@app.route('/search', methods=['GET'])
def search():
    logging.info("Accessed the /search route")
    query = request.args.get('query')
    search_option = request.args.get('search_option')
    sort_by = request.args.get('sort_by')
    algorithm = request.args.get('algorithm')

    logging.debug(f"Received search query: {query}")
    logging.debug(f"Search option: {search_option}")
    logging.debug(f"Sort by: {sort_by}")
    logging.debug(f"Algorithm: {algorithm}")

    if algorithm == 'boolean':
        return boolean_search(query, search_option, algorithm, data_sets['paper_processed_data'],
                              data_sets['paper_data'], sort_by)
    elif algorithm == 'vector_space':
        return vector_space_search(query, search_option, algorithm, data_sets['paper_processed_data'],
                                   data_sets['paper_data'], sort_by)
    elif algorithm == 'probabilistic':
        return probabilistic_search(query, search_option, algorithm, data_sets['paper_processed_data'],
                                    data_sets['paper_data'], sort_by)
    else:
        return simple_search(query, search_option, algorithm, data_sets['author_data'], data_sets['date_data'],
                             data_sets['abstract_data'], data_sets['title_data'], data_sets['paper_data'], sort_by)
