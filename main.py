from modules.logging import logging_function
from modules.extract import extract_function
from modules.load import load_function
from datetime import datetime
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()

aws_access_key_id = os.getenv('aws_access_key_id')
aws_secret_access_key = os.getenv('aws_secret_access_key')
bucket_name = os.getenv('bucket_name')

timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
url = 'https://api.tfl.gov.uk/BikePoint'

extract_logger = logging_function('extract',timestamp)

extract_function(url,3, extract_logger, timestamp)

load_logger = logging_function('load',timestamp)

load_function(Path('data'), aws_access_key_id, aws_secret_access_key, bucket_name, load_logger)
