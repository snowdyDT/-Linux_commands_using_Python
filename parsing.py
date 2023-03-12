import requests
import config

endpoint = config.endpoint


data = requests.get(endpoint).text
print(data)
