import logging
import sys


def configure_main_logging(log_path):
    """
    Configures the main logging for the application.

    Parameters:
    - log_path (str): The file path to save the log file.

    Returns:
    - None
    """
    logging.basicConfig(
        filename=log_path,
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Create a StreamHandler to print logs to the terminal
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    console_handler.setFormatter(formatter)

    # Add the StreamHandler to the logging configuration
    logging.getLogger().addHandler(console_handler)
