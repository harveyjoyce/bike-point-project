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

main.py
- This is the main script you run.


<ol>
  <li>Sends a GET request to the TfL BikePoint API: <code>https://api.tfl.gov.uk/BikePoint</code></li>
  <li>Retries the request up to <strong>3 times</strong> if an unsuccessful response is received</li>
  <li>On success:
    <ul>
      <li>Saves the response as a JSON file in the <code>data/</code> directory</li>
      <li>Creates a timestamped log file in the <code>logs/</code> directory</li>
    </ul>
  </li>
  <li>Logs system activity at INFO level and above</li>
</ol>

<h3>Script B – Upload JSON to S3 (<code>load_bike_points.py</code>)</h3>
<ol>
  <li>Loads AWS credentials from <code>.env</code></li>
  <li>Searches for all JSON files in the <code>data/</code> directory</li>
  <li>Raises an error if no files are found</li>
  <li>Uploads each JSON file to the specified S3 bucket</li>
  <li>Deletes local JSON files after a successful upload</li>
  <li>Logs all upload actions and errors to timestamped files in <code>load_logs/</code></li>
</ol>

<hr>

<h2>Logging</h2>
<p>Each script execution creates a log file containing:</p>
<ul>
  <li>System status messages</li>
  <li>Successful downloads/uploads</li>
  <li>Warnings and errors</li>
  <li>Critical failures</li>
</ul>

<p>Example log entry:</p>
<pre><code>2026-01-07 12:30:01 - INFO - Download successful at 2026-01-07 12-30-01 😊
2026-01-07 12:35:15 - INFO - Uploaded and deleted: 2026-01-07 12-30-01.json
</code></pre>

<hr>

<h2>Usage</h2>

<h3>Download BikePoint Data</h3>
<pre><code>python extract_bike_points.py</code></pre>
<p>On successful execution:</p>
<ul>
  <li>A JSON file will be saved in the <code>data/</code> folder</li>
  <li>A log file will be saved in the <code>logs/</code> folder</li>
  <li>A success message will be printed to the console</li>
</ul>

<h3>Upload JSON Files to S3</h3>
<pre><code>python load_bike_points.py</code></pre>
<p>On successful execution:</p>
<ul>
  <li>JSON files will be uploaded to your S3 bucket</li>
  <li>Local copies of the files will be deleted</li>
  <li>A log file will be saved in the <code>load_logs/</code> folder</li>
</ul>

<hr>

<h2>API Reference</h2>
<p>TfL BikePoint API documentation:<br>
<a href="https://api.tfl.gov.uk/swagger/ui/#!/BikePoint/BikePoint_GetAll">https://api.tfl.gov.uk/swagger/ui/#!/BikePoint/BikePoint_GetAll</a></p>

<hr>

<h2>Error Handling</h2>
<ul>
  <li>HTTP status codes outside the successful range trigger a retry</li>
  <li>Requests time out after 10 seconds</li>
  <li>All errors are logged for troubleshooting</li>
  <li>S3 upload errors are logged, and execution stops if no JSON files are found</li>
</ul>

<hr>

<hr>

<h2>License</h2>
<p>This project uses public TfL API data and is intended for educational and non-commercial use.<br>
Please refer to TfL’s API terms and conditions for usage guidelines.</p>
