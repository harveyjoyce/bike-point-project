import boto3
import os
from botocore.exceptions import BotoCoreError, ClientError
import logging

def load_function(data_dir, aws_access_key_id, aws_secret_access_key, bucket_name, logger):
    '''
    Loads json data from data_dir to s3 bucket
    
    :param data_dir: Description
    :param access_key: Description
    :param secret_access_key: Description
    :param bucket: Description
    :param logger: Description
    '''

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


