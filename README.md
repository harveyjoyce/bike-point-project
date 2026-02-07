# BikePoint (TfL) Project 🚲

<img align="right" alt="image" src="https://github.com/user-attachments/assets/c54d8d3a-6018-4f5f-97ae-2f5af6e904a9" width="30%"/>

This project: 
- Retrieves live Santander Cycle hire (BikePoint) data from the **[Transport for London (TfL) BikePoint API](https://api.tfl.gov.uk/swagger/ui/index.html#!/BikePoint/BikePoint_GetAll)**
- Logs execution details, stores the downloaded data locally as timestamped JSON files
- Uploads them to an S3 bucket in **AWS** which connects to **Snowflake**
- **dbt** is used to parse out the raw JSON 

## Project Overview Diagram 🎨

<img width="3452" height="1323" alt="image" src="https://github.com/user-attachments/assets/030140a4-2b3c-40d2-8bbf-780bdabf41a7" />

## Setting up the Repository ⚙️

1. Clone this repository:

```bash
git clone https://github.com/yourusername/bike-point-project.git
```

2. Create a branch

```bash
git checkout -b your-branch-name
```

3. Create and activate a virtual environment:

```bash
python -m venv .venv
# Linux / Mac
source .venv/bin/activate
# Windows
.venv\Scripts\activate
```

3. Install required packages

```bash
pip install -r requirements.txt
```

4. Add a .env file in the root of the project containing your AWS credentials (After setting up an appropriate IAM User and S3 Bucket):

```
aws_access_key_id = ' '
aws_secret_access_key = ' '
bucket_name = ' '
```

## Project Structure 👷‍♂️

```
├── data/
│   └── YYYY-MM-DD HH-MM-SS.json
├── extract_logs/
│   └── YYYY-MM-DD HH-MM-SS.log
├── load_logs/
│   └── YYYY-MM-DD HH-MM-SS.log
├── main.py
├── modules/
│   └── logging.py
│   └── extract.py
│   └── load.py
├── archive/
│   └── extract_bike_points.py
│   └── load_bike_points.py
├── .env
└── README.md
```

## How It Works 🔨

**main.py**

This script acts as the orchestrator for a data pipeline, moving BikePoint data to S3. Here is what it's doing:
- Environment & Setup: It loads secure credentials (AWS keys) from a .env file and initialises two distinct logging sessions—one for `extract` and one for `load`—using the current timestamp.
- Data Extraction: It triggers a process to fetch bike point data from the TfL API and passes the `extract_logger` to track the success or failure of that specific task.
- Cloud Loading: It takes the locally saved data from a data folder and uploads it to a specified AWS S3 bucket, using the `load_logger` to record the transfer details.

**logging.py**

This script sets up a reusable logging system in Python. Here is the breakdown of what it’s doing:
- Creates a Directory: It automatically generates a folder named after your prefix (if it doesn't already exist) to store your log files.
- Initialises a File Logger: It creates a specific .log file named with your timestamp and configures it to record messages at the INFO level.
- Prevents Duplication: It checks for existing "handlers" before adding new ones, ensuring your logs don't accidentally double-post the same message to the file.

**extract.py**

This script handles the extraction and storage phase of your pipeline with built-in error handling. Here is what’s happening:
- API Request with Retry Logic: It attempts to fetch data from the provided URL and is programmed to retry up to a specific number of times if it encounters server errors (status codes 500+) or connection issues.
- JSON File Management: Upon a successful "200 OK" response, it ensures a `data` directory exists and saves the API results as a local .json file named after the current timestamp.
- Success and Error Logging: It records the outcome of the attempt—logging a success message and a "😊" emoji to your log file if it works, or capturing the failure reason if the request hits a permanent error (like a 404).
- It will try 3 times in total, waiting 10 seconds each go (`time.sleep(10)`).

**load.py**

This script handles the loading and cleanup phase of your pipeline, moving local data to the cloud. Here is what it’s doing:
- File Discovery & Validation: It scans the `data` directory for all files ending in .json; if it doesn't find any, it logs an error and stops the process to prevent unnecessary cloud connections.
- S3 Cloud Upload: Using the `boto3` library, it establishes a connection to AWS and uploads each JSON file to your specified S3 bucket using the original filename.
- Cleanup & Error Logging: After a successful upload, it deletes the local file (`unlink`) to save space; if an upload fails due to AWS permissions or network issues, it catches the error and logs it without crashing the entire loop.

## Logging 📝
Each script execution creates a log file containing:
- System status messages
- Successful downloads/uploads
- Warnings and errors
- Critical failures

Example log entry:
```
2026-01-07 12:30:01 - INFO - Download successful at 2026-01-07 12-30-01 😊
2026-01-07 12:35:15 - INFO - Uploaded and deleted: 2026-01-07 12-30-01.json
```

## License 🪪 

This project uses public TfL API data and is intended for educational and non-commercial use.
Please refer to TfL’s API terms and conditions for usage guidelines.

## Configuring AWS 🟧 and Snowflake ❄️

To connect to Snowflake from AWS, you need to create an IAM Role and Storage Intergration. I have written a blog [here](https://www.thedataschool.co.uk/harvey-joyce/connecting-snowflake-and-aws-s3-storage-integration-and-procedures/) on how to set that up!

## dbt Project Structure 🟠

```
├── analyses/             # SQL files for one-off exports or ad-hoc queries
├── macros/               # Reusable Jinja functions (like custom aggregations)
├── models/               # The heart of your project
│   ├── staging/          # Raw data cleaning (renaming, type casting)
│   │   └── bike_point/   # Organized by source system (e.g., stripe, hubspot)
│   │       ├── base/
│   │       │    └── base_bike_point__parsed.sql
│   │       ├── _bike_point__sources.yml
│   │       └── stg_bike_point__parsed.sql
│   ├── intermediate/     # Complex joins and business logic between staging/marts
│   └── marts/            # Final, "gold" tables for BI tools
│       └── bike_point/
│           ├── bike_point_gold.sql
│           ├── dim_bike_point.sql
│           └── fct_bike_point.sql
├── seeds/                # Small, static CSV files (e.g., country codes)
├── snapshots/            # Files for tracking data changes over time (SCD Type 2)
├── tests/                # Custom data quality tests (singular tests)
├── dbt_project.yml       # The main configuration file for the whole project
├── packages.yml          # External dbt libraries (like dbt-utils)
├── profiles.yml          # Connection credentials (usually kept in ~/.dbt/)
└── README.md
```
