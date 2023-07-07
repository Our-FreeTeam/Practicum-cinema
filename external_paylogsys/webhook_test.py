import requests
import json

# The URL of your Flask app's /webhook endpoint
url = 'https://yptst2023.omnitoring.ru:5005/webhook'

# The data you want to send
data = {
    'key1': 'value1',
    'key2': 'value2',
    'key3': 'value3'
}

# Send the POST request
response = requests.post(url, data=json.dumps(data), headers={'Content-Type': 'application/json'})

# Print the response
print(response.text)
