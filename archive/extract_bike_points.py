import requests
import os
from datetime import datetime
import json
import time
import logging

logs_dir = 'logs'
if os.path.exists(logs_dir):
    pass
else:
    os.mkdir(logs_dir)
filename = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
log_filename = f"logs/{filename}.log"

# Configure logs to retrieve INFO messages and higher
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=log_filename
)

logger = logging.getLogger()

#Add the following to your script when you want logging to occur:
logger.debug("This is a debug message")    
logger.info("System working")            
logger.warning("Something unexpected")        
logger.error("An error occurred")             
logger.critical("Critical system error")

# Documentation here: https://api.tfl.gov.uk/swagger/ui/#!/BikePoint/BikePoint_GetAll 
url = 'https://api.tfl.gov.uk/BikePoint'

response = requests.get(url,timeout=10)
response_code = response.status_code

count = 0
number_of_tries = 3

while count < number_of_tries:

    response = requests.get(url,timeout=10)
    response_code = response.status_code

    if response_code==200:
        response_json = response.json()

        #We need to check if the directory exists and make it if not
        dir = 'data'
        if os.path.exists(dir):
            pass
        else:
            os.mkdir(dir)

        filepath = f'{dir}/{filename}.json'

        try:
            with open(filepath,'w') as file:
                json.dump(response_json, file)
            print(f'Download successful at {filename} 😊')
            logger.info(f'Download successful at {filename} 😊')
        except Exception as e:
            print(e)

        break

    elif response_code>499 or response_code<200:
        #retry
        time.sleep(10)
        count+=1
    else: 
        print(response.reason)
        logger.error(response.reason)
        break