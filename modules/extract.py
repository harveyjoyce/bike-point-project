import requests
import json
import os
import time


def extract_function(url, number_of_tries, logger, timestamp):
    '''
    Designed for extracting data from bike point API
    
    :param url: Description
    :param number_of_tries: Description
    :param logger: Description
    :param timestamp: Description
    '''
    count = 0

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

            filepath = f'{dir}/{timestamp}.json'

            try:
                with open(filepath,'w') as file:
                    json.dump(response_json, file)
                print(f'Download successful at {timestamp} 😊')
                logger.info(f'Download successful at {timestamp} 😊')
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