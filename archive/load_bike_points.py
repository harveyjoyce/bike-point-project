import boto3
from dotenv import load_dotenv
import os
from pathlib import Path
from botocore.exceptions import BotoCoreError, ClientError
from datetime import datetime
import logging

# Create directories if necessary 
logs_dir = 'load_logs'
if os.path.exists(logs_dir):
    pass
else:
    os.mkdir(logs_dir)
filename = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
log_filename = f"load_logs/{filename}.log"

# Configure logs to retrieve INFO messages and higher
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=log_filename
)

logger = logging.getLogger()

load_dotenv()

aws_access_key_id = os.getenv('aws_access_key_id')
aws_secret_access_key = os.getenv('aws_secret_access_key')
bucket_name = os.getenv('bucket_name')
logger.info("Environment Variables Read")

data_dir = Path('data')

# Find JSON files
json_files = list(data_dir.glob('*.json'))

# Error if no files exist
if not json_files:
    logger.error("No JSON files found")
    raise FileNotFoundError(f"No JSON files found in '{data_dir}'")


s3_client = boto3.client(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)

# Loop through each JSON file and upload it to S3
for json_file in json_files:
    try:
        # Upload the file to the specified S3 bucket
        s3_client.upload_file(
            str(json_file),  # File path as a string
            bucket_name,     # S3 bucket name
            json_file.name   # Name of the file in S3
        )

        # Delete the local file after successful upload
        json_file.unlink()
        logger.info(f"Uploaded and deleted: {json_file.name}")

    # Handle known AWS errors
    except (BotoCoreError, ClientError) as e:
        logger.error(f"Failed to upload {json_file.name}: {e}")

    # Handle any other unexpected errors
    except Exception as e:
        logger.error(f"Unexpected error with {json_file.name}: {e}")
