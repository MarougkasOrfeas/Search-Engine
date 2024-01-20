import json
import logging


def json_read(file_path):
    """
        Read data from a JSON file.

        Parameters:
        - file_path (str): The path to the JSON file.

        Returns:
        - data: The data read from the JSON file.
        """
    try:
        with open(file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        return data
    except FileNotFoundError:
        logging.warning(f"File not found: {file_path}")
        return None
    except Exception as e:
        logging.error(f"Error reading JSON from {file_path}: {e}")
        return None


def json_write(data, file_path):
    """
        Write data to a JSON file.

        Parameters:
        - data: The data to be written to the JSON file.
        - file_path (str): The path to the JSON file.
        """
    try:
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        logging.info(f"Data written to {file_path}...")
    except Exception as e:
        logging.error(f"Error writing JSON to {file_path}: {e}")


def load_data(data):
    return {key: json_read(path.value) for key, path in data.items()}
