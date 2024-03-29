# Imports taken from https://docs.ckan.org/en/2.9/api/, the documentation for the
# CKAN API, used by Boston 311

import urllib
from urllib.parse import urlparse
import json
import pprint
import requests
from requests.structures import CaseInsensitiveDict


def find_issues(address):
    # This method will take some address, find the longitude and lattitude
    # with the geocoder API, then search the 311 data for relevant hits within
    # one city block.

    # This structure taken from https://docs.ckan.org/en/2.9/api/. Modified.
    dataset_dict = {
        'name': 'boston311',
        'notes': 'This dataset contains all (unfiltered) data from the Boston 311 API in 2023',
        'owner_org': 'analyze_boston' #??
    }

    latlong = address_to_latlong(address)
    # Should dump the dictionary into a string ("for posting")
    data_string = urllib.parse.urlparse(json.dumps(dataset_dict))

    url = 'https://data.boston.gov/api/3/action/datastore_search'
    headers = {'Authorization': 'df608ec0-f746-49a2-b91b-6d306742d07e'}
    params = {'longitude' : -71.08691933926416}
    

    # Open the API (url found at Boston 311, marked Create)
    response = requests.get(url, headers=headers, params=params)
    dict = response.json()

    # This should be the autorization key -- ???

    # request.headers('Authorization', 'df608ec0-f746-49a2-b91b-6d306742d07e')


    # Then, we make the HTTP request. We are asserting the response is 200 because that is
    # CKAN's success marker
    print(response.json())
    # assert response.code == 200
    return




def address_to_latlong (address):
    #We have to first open the geocoder API to convert the address to coordinates
    # In this implementation, the user is asked to enter each specific parameter of 
    # their address. The geocoder API we are using also allows for text parsing, 
    # which is implemented below

    geocoder_key = '3a16f8a827ad4f479822ac182bc7f694'
    
    url = "https://api.geoapify.com/v1/geocode/search?&apiKey="

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"

    params =  {
        'text' : address
    }

    response = requests.get(url+geocoder_key, headers=headers, params=params)
    file = response.json()
    #print(find_by_key(file, "lat"))
    print(type(file['features'][0]))

    latlong = {
        "long" : 0,
        "lat" : 0
    }
    latlong['long'] = find_by_key(file['features'][0]['properties'], 'lon')
    latlong['lat'] = find_by_key(file['features'][0]['properties'], 'lat')

    return latlong
    


def find_by_key(data, target): 
    for key, value in data.items():        
        if key == target:
            return value
   




find_issues("98 Mountfort street, boston, 02215 massachusetts, united states of america")