# Search Engine For Academic Papers
## Introduction
This is a simple search engine for academic papers on <b>arXiv </b>. The search engine allows users to perform queries and retrieve relevant academic papers based on various search options and algorithms. The system includes a web crawler to fetch arXiv papers, and it supports different search algorithms such as Boolean Search, Vector Space Model, and Probabilistic Retrieval.

## Features
* <b>Web Crawler:</b> The system includes a web crawler that fetches academic papers from arXiv based on user queries.

* <b>Search Options:</b> Users can choose different search options, including searching in specific fields such as Authors, Date, Abstract, Title, or searching in all fields simultaneously.
* <b>Sorting:</b> Users can sort search results based on Date, Authors, or Title.
* <b>Search Algorithms:</b>
  * <b>Boolean Search:</b> Supports queries with Boolean operators (AND, OR, NOT) for more refined searches.
  * <b>Vector Space Model:</b> Utilizes TF-IDF (Term Frequency-Inverse Document Frequency) and cosine similarity for searching and ranking.
  * <b>Probabilistic Retrieval:</b> Uses the BM25 algorithm to calculate scores and rank documents.


## How to Use
1) Install Dependencies:
   * Make sure you have Python installed.
   * Install the required packages using: pip install -r requirements.txt.
2) Run the Application:
   * Execute the app.py file to start the Flask application.
   * Access the search engine in your web browser at http://localhost:5000.
3) Perform Searches:
   * Enter your search query and select search options.
   * Choose a search algorithm and sorting option.
   * Click the "Search" button to see the results.
4) Crawl New Papers:
   * Access the "/crawl" route to fetch new academic papers based on a query.
   * Provide the query and the maximum number of results.
## Directory Structure
* templates: Contains HTML templates for rendering the web pages.
* utils: Includes utility functions for logging, data loading, and processing.
* crawler: Contains the web crawler and preprocessing functions.
* exceptions: Holds custom exception classes.
## Notes
This application uses Flask as the web framework.
Logging is configured for better tracking of events and errors.
Data is stored in JSON files, and inverted indices are created for efficient searching.

## Acknowledgments
This project was developed as part of a learning exercise in the University of West Attica.