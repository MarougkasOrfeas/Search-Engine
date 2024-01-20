import logging
import re

from rank_bm25 import BM25Okapi
from flask import render_template
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils.utils import sort_results, inverted_index_search


def vector_space_search(query, search_option, algorithm, paper_processed_data, paper_data, sort_by):
    """
    Perform vector space search algorithm.

    Parameters:
    - query: User's search query.
    - search_option: Search option ('all_fields' or specific field like 'Authors', 'Date', 'Abstract', 'Title').
    - algorithm: Search algorithm ('vector_space').
    - paper_processed_data: Processed paper data.
    - paper_data: Original paper data.
    - sort_by: Sorting option ('date', 'author', 'title').

    Returns:
    - Rendered template with search results.
    """
    logging.info("Entered vector space algorithm")

    # Construct corpus and query_data based on search_option
    if search_option == 'all_fields':
        corpus = [' '.join([paper['Title_processed'], paper['Authors_processed'], paper['Abstract_processed'],
                            paper['Date_processed']]) for paper in paper_processed_data]
        query_data = ' '.join([query])
    else:
        corpus = [' '.join([paper[f'{search_option}_processed']]) for paper in paper_processed_data]
        query_data = ' '.join([query])

    # Create TF-IDF matrix and compute similarities
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus + [query_data])
    similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
    ranking = similarities.argsort()[0][::-1]
    papers_to_display = [paper_data[index] for index in ranking]

    # Sort the filtered papers
    papers_to_display = sort_results(papers_to_display, sort_by)
    logging.debug(f"Matching documents: {papers_to_display}")

    return render_template('results.html', query=query, search_option=search_option,
                           algorithm=algorithm, results=papers_to_display)


def probabilistic_search(query, search_option, algorithm, paper_processed_data, paper_data, sort_by):
    """
    Perform probabilistic search algorithm.

    Parameters:
    - query: User's search query.
    - search_option: Search option ('all_fields' or specific field like 'Authors', 'Date', 'Abstract', 'Title').
    - algorithm: Search algorithm ('probabilistic').
    - paper_processed_data: Processed paper data.
    - paper_data: Original paper data.
    - sort_by: Sorting option ('date', 'author', 'title').

    Returns:
    - Rendered template with search results.
    """
    logging.info("Entered probabilistic algorithm")

    # Construct corpus and query_data based on search_option
    if search_option == 'all_fields':
        corpus = [' '.join([paper['Title_processed'], paper['Authors_processed'], paper['Abstract_processed'],
                            paper['Date_processed']]) for paper in paper_processed_data]
        query_data = ' '.join([query])
    else:
        corpus = [' '.join([paper[f'{search_option}_processed']]) for paper in paper_processed_data]
        query_data = ' '.join([query])

    # Create BM25 model and compute similarities
    bm25 = BM25Okapi([doc.split() for doc in corpus])
    similarities = bm25.get_scores(query_data.split())
    ranking = sorted(range(len(similarities)), key=lambda i: similarities[i], reverse=True)
    papers_to_display = [paper_data[index] for index in ranking]

    # Sort the filtered papers
    papers_to_display = sort_results(papers_to_display, sort_by)
    logging.debug(f"Matching documents: {papers_to_display}")

    return render_template('results.html', query=query, search_option=search_option,
                           algorithm=algorithm, results=papers_to_display)


def simple_search(query, search_option, algorithm, author_data, date_data, abstract_data, title_data, paper_data,
                  sort_by):
    """
    Perform simple search algorithm.

    Parameters:
    - query: User's search query.
    - search_option: Search option ('Authors', 'Date', 'Abstract', 'Title', 'all_fields').
    - algorithm: Search algorithm ('simple' in this case).
    - author_data: Data for the 'Authors' field.
    - date_data: Data for the 'Date' field.
    - abstract_data: Data for the 'Abstract' field.
    - title_data: Data for the 'Title' field.
    - paper_data: Original paper data.
    - sort_by: Sorting option ('date', 'author', 'title').

    Returns:
    - Rendered template with search results.
    """
    logging.info("Entered simple search")

    if query and search_option:
        logging.info(f"Performing search with option: {search_option}")

        if search_option == 'Authors':
            logging.debug("Search option: Authors")
            matching_documents = inverted_index_search(query, author_data)
        elif search_option == 'Date':
            logging.debug("Search option: Date")
            matching_documents = inverted_index_search(query, date_data)
        elif search_option == 'Abstract':
            logging.debug("Search option: Abstract")
            matching_documents = inverted_index_search(query, abstract_data)
        elif search_option == 'Title':
            logging.debug("Search option: Title")
            matching_documents = inverted_index_search(query, title_data)
        else:  # Default to 'all_fields' or any other case
            logging.debug("Search option: all_fields")
            matching_documents = inverted_index_search(query, author_data) + \
                                 inverted_index_search(query, date_data) + \
                                 inverted_index_search(query, abstract_data) + \
                                 inverted_index_search(query, title_data)

        logging.info(f"Matching documents: {matching_documents}")

        papers_to_display = [paper_data[idx] for idx in matching_documents]
        logging.debug(f"Matching documents: {papers_to_display}")

        # Sort the filtered papers
        papers_to_display = sort_results(papers_to_display, sort_by)
        logging.debug(f"Final results: {papers_to_display}")

        return render_template('results.html', query=query, search_option=search_option,
                               algorithm=algorithm, results=papers_to_display)


def boolean_search(query, search_option, algorithm, paper_processed_data, paper_data, sort_by):
    logging.info("Entered boolean algorithm")
    matching_documents = []
    if 'AND' in query or 'OR' in query or 'NOT' in query:
        split_query = re.split(r'(AND|OR|NOT)', query)
        logging.info(f"Split query into terms and operators: {split_query}")
        terms_and_operators = [term.strip() for term in split_query if term.strip()]

        terms = []
        operators = []
        queries = []

        for item in terms_and_operators:
            if item in {'AND', 'OR', 'NOT'}:
                operators.append(item)
            else:
                terms.append(item.lower().replace(" ", ""))
        logging.debug(f"Query terms: {terms}")
        logging.debug(f"Query operators: {operators}")
        for i in range(1, len(terms)):
            query_string = f"{terms[i - 1]} {operators[i - 1]} {terms[i]}"
            queries.append(query_string)
        logging.info(f"Generated queries: {queries}")

        for query in queries:
            if 'AND' in query:
                terms = query.split(' AND ')
                term1 = terms[0]
                term2 = terms[1]
                logging.debug(f"terms1: {term1}")
                logging.debug(f"terms2: {term2}")

                for paper in paper_processed_data:
                    if search_option == 'all_fields':
                        if term1 in paper['Title_processed'] or term1 in paper['Authors_processed'] or term1 in \
                                paper[
                                    'Abstract_processed'] or term1 in paper['Date_processed']:
                            matching_documents.append(paper['ID'])
                    else:
                        if term1 in paper[f'{search_option}_processed']:
                            matching_documents.append(paper['ID'])
                # print(f"Matching documents term1{matching_documents}")
                final_matching_documents = []
                for paper_id in matching_documents:
                    paper = paper_processed_data[
                        paper_id - 1]
                    if search_option == 'all_fields':
                        if term2 in paper['Title_processed'] or term2 in paper['Authors_processed'] or term2 in \
                                paper[
                                    'Abstract_processed'] or term2 in paper['Date_processed']:
                            final_matching_documents.append(paper_id)
                    else:
                        if term2 in paper[f'{search_option}_processed']:
                            final_matching_documents.append(paper_id)

                logging.info(f"Final matching documents: {final_matching_documents}")
                papers_to_display = [paper_data[paper_id - 1] for paper_id in final_matching_documents]
                logging.debug(f"papers_to_display: {papers_to_display}")
                # Sort the filtered papers
                papers_to_display = sort_results(papers_to_display, sort_by)
                return render_template('results.html', query=query, search_option=search_option,
                                       algorithm=algorithm, results=papers_to_display)
            elif 'OR' in query:
                terms = query.split(' OR ')
                term1 = terms[0]
                term2 = terms[1]
                logging.debug(f"terms1: {term1}")
                logging.debug(f"terms2: {term2}")

                for paper in paper_processed_data:
                    if term1 in paper['Title_processed'] or term1 in paper['Authors_processed'] or term1 in paper[
                        'Abstract_processed'] or term1 in paper['Date_processed'] or term2 in paper[
                        'Title_processed'] or term2 in paper['Authors_processed'] or term2 in paper[
                        'Abstract_processed'] or term2 in paper['Date_processed']:
                        matching_documents.append(paper['ID'])

                if not matching_documents:
                    for paper in paper_processed_data:
                        if term2 in paper['Title_processed'] or term2 in paper['Authors_processed'] or term2 in \
                                paper['Abstract_processed'] or term2 in paper['Date_processed']:
                            matching_documents.append(paper['ID'])

                logging.info(f"Final matching documents term1 OR term2: {matching_documents}")
                final_matching_documents = []

                for paper_id in matching_documents:
                    paper = paper_processed_data[paper_id - 1]
                    final_matching_documents.append(paper_id)
                    logging.debug(f"Match found for term1 OR term2 in paper {paper_id}")

                logging.info(f"Final matching documents: {final_matching_documents}")
                papers_to_display = [paper_data[paper_id - 1] for paper_id in final_matching_documents]
                logging.debug(f"papers_to_display: {papers_to_display}")
                # Sort the filtered papers
                papers_to_display = sort_results(papers_to_display, sort_by)
                return render_template('results.html', query=query, search_option=search_option,
                                       algorithm=algorithm, results=papers_to_display)
            elif 'NOT' in query:
                terms = query.split(' NOT ')
                term1 = terms[0]
                term2 = terms[1]
                logging.debug(f"terms1: {term1}")
                logging.debug(f"terms2: {term2}")

                matching_documents_term1 = []

                for paper in paper_processed_data:
                    if term1 in paper['Title_processed'] or term1 in paper['Authors_processed'] or term1 in paper[
                        'Abstract_processed'] or term1 in paper['Date_processed']:
                        matching_documents_term1.append(paper['ID'])

                matching_documents_term2 = []

                for paper in paper_processed_data:
                    if term2 in paper['Title_processed'] or term2 in paper['Authors_processed'] or term2 in paper[
                        'Abstract_processed'] or term2 in paper['Date_processed']:
                        matching_documents_term2.append(paper['ID'])

                matching_documents = list(set(matching_documents_term1) - set(matching_documents_term2))
                logging.info(f"Final matching documents term1 NOT term2: {matching_documents}")
                final_matching_documents = []

                for paper_id in matching_documents:
                    paper = paper_processed_data[paper_id - 1]
                    final_matching_documents.append(paper_id)
                    logging.debug(f"Match found for term1 NOT term2 in paper {paper_id}")

                logging.info(f"Final matching documents: {final_matching_documents}")
                papers_to_display = [paper_data[paper_id - 1] for paper_id in final_matching_documents]
                logging.debug(f"papers_to_display: {papers_to_display}")
                # Sort the filtered papers
                papers_to_display = sort_results(papers_to_display, sort_by)
                return render_template('results.html', query=query, search_option=search_option,
                                       algorithm=algorithm, results=papers_to_display)

    else:
        return []
