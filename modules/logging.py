import logging
import os
from datetime import datetime

def logging_function(prefix, timestamp):
    '''
    Designed for logging
    
    :param prefix: For folder name of lof
    :param timestamp: for name of log files
    '''

    dir = f'{prefix}_logs'
    os.makedirs(dir, exist_ok=True)

    log_filename = f"{dir}/{timestamp}.log"

    # Create a unique logger for this prefix
    logger = logging.getLogger(prefix)
    logger.setLevel(logging.INFO)

    # Check if logger already has handlers to prevent duplicate logs
    if not logger.handlers:
        # Create file handler
        file_handler = logging.FileHandler(log_filename)
        
        # Create formatter and add it to the handler
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        # Add the handler to the logger
        logger.addHandler(file_handler)

    return logger
