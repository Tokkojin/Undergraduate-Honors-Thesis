# Hayden Le

# import urllib3
import certifi
import requests
import json

# http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

washington_post_search = 'https://sitesearchapp.washingtonpost.com/sitesearch-api/v2/search.json'
data = {
        'query': 'harvey+weinstein',
        'count': 1000,
        }

# how many results?
print(json.loads(response.text)['results']['total'] + ' articles found.')

response = requests.post(washington_post_search, data =data)

# print(json.loads(response.text))
i = 1
for item in json.loads(response.text)['results']['documents']:
    print(item['contenturl'])
    print(i)
    i = i + 1

