from utils.json_config import json_write
import logging


def create_and_save_inverted_index(data, field_name, output_file):
    """
    Creates and saves an inverted index for a specific field in the given data.

    Parameters:
    - data (list): List of items containing the field for which the inverted index needs to be created.
    - field_name (str): The field name for which the inverted index is created.
    - output_file (str): The file path to save the inverted index.

    Returns:
    - None
    """
    # logging.info(f"Creating and saving inverted index for {field_name}...")
    inverted_index = {}
    for idx, item in enumerate(data):
        if field_name in item:
            terms = item[field_name].split()
            for term in set(terms):
                if term not in inverted_index:
                    inverted_index[term] = {'documents': [idx]}
                else:
                    inverted_index[term]['documents'].append(idx)

    json_write(inverted_index, output_file)
    logging.info(f"Successfully created and saved all inverted index for {field_name} ({len(data)} items).")
