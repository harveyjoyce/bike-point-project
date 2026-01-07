import requests
import os
from datetime import datetime
import json

# Documentation here: https://api.tfl.gov.uk/swagger/ui/#!/BikePoint/BikePoint_GetAll 
url = 'https://api.tfl.gov.uk/BikePoint'

response = requests.get(url,timeout=10)
response_json = response.json()

#We need to check if the directory exists and make it if not
dir = 'data'
if os.path.exists(dir):
    pass
else:
    os.mkdir(dir)

filename = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
filepath = f'{dir}/{filename}.json'

with open(filepath,'w') as file:
    json.dump(response_json, file)

print(f'Download successful at {filename} 😊')