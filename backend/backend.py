# Imports taken from https://docs.ckan.org/en/2.9/api/, the documentation for the
# CKAN API, used by Boston 311

import urllib
from urllib.parse import urlparse
import json
import pprint
import requests

# This structure also taken from https://docs.ckan.org/en/2.9/api/. Modified.
dataset_dict = {
    'name': 'boston311',
    'notes': 'This dataset contains all (unfiltered) data from the Boston 311 API in 2023',
    'owner_org': 'analyze_boston' #??
}

# Should dump the dictionary into a string ("for posting")
data_string = urllib.parse.urlparse(json.dumps(dataset_dict))

url = 'https://data.boston.gov/api/3/action/datastore_search'
headers = {'Authorization': 'df608ec0-f746-49a2-b91b-6d306742d07e'}

# Open the API (url found at Boston 311, marked Create)
response = requests.get(url, headers=headers)

# This should be the autorization key -- ???

# request.headers('Authorization', 'df608ec0-f746-49a2-b91b-6d306742d07e')


# Then, we make the HTTP request. We are asserting the response is 200 because that is
# CKAN's success marker
print(response.json())
# assert response.code == 200