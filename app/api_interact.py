import urllib
from urllib.parse import urlparse
import json
import pprint
import requests
from requests.structures import CaseInsensitiveDict



def find_issues_wrapper(address):
    # Public keys found on the Boston311 website
    key_2023 = ('2023', 'e6013a93-1321-4f2a-bf91-8d8a02f1e62f')
    key_2022 = ('2022','81a7b022-f8fc-4da5-80e4-b160058ca207')
    key_2021 = ('2021','f53ebccd-bc61-49f9-83db-625f209c95f5')
    key_2020 = ('2020','6ff6a6fd-3141-4440-a880-6f60a37fe789')
    key_2019 = ('2019','ea2e4696-4a2d-429c-9807-d02eb92e0222')

    keys = [key_2019, key_2020, key_2021, key_2022, key_2023]
    reports = {}
    for year,key in keys:
        report = find_issues(address, key)
        if report == -1:
            return -1
        reports['report' + year] = report

    return reports


def find_issues(address,key):
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
    if latlong == -1:
        return -1

    lon1 = str((latlong["long"] + 0.000225)) 
    lon2 = str(latlong["long"] - 0.000225) 
    # lon1 = "-71.03749937922044"
    # lon2 = "-71.03749937922046"
    lat1 = str(latlong["lat"] + 0.000225)
    lat2 = str(latlong["lat"] - 0.000225)
    # lat1= "42.36775149266105"
    # lat2 =  "42.36775149266103"
    while len(lon1)<18:
        lon1 = lon1+"0"
    while len(lon2)<18:
        lon2 = lon2+"0"

    # 14 decimal points
    # SELECT * from "e6013a93-1321-4f2a-bf91-8d8a02f1e62f" WHERE ('lattitude' BETWEEN '-71.08692220816602' AND '-71.08692220816604') AND ('longitude' BETWEEN '42.29817900658342' AND '42.29817900658344')

    params = urllib.parse.urlencode(dataset_dict, doseq=True)
    url = 'https://data.boston.gov/api/3/action/datastore_search_sql?sql=SELECT%20*%20from%20%22' + key + '%22%20WHERE%20%22longitude%22%20BETWEEN%20%27' + lon1 + '%27%20AND%20%27' + lon2 + '%27'
    response = requests.get(url)
    data = response.json()
    filtered_data = []
    for item in data['result']['records']:
        if item['latitude'] < lat1 and item['latitude'] > lat2:
            filtered_data.append(item)
    
    report = []
   
    # Boston311 issues deemed relevant to apartment conditions
    hit_list_5 = ["Aircraft Noise Disturbance", "Animal Noise Disturbances", "Automotive Noise Disturbance", 
                   'Dumpster & Loading Noise Disturbances', "Loud Parties/Music/People", "Undefined Noise Disturbance", "Unshoveled Sidewalk"]
    hit_list_1 = ["Improper Storage of Trash (Barrels)", "No Utilities Residential - Gas", "No Utilities Residential - Electricity",
                   "No Utilities Residential - Water", "Student Move-in Issues", "Student Overcrowding", "Unsatisfactory Utilities - Electrical Plumbing"]
    hit_list_3 = [ "Bed Bugs", "Mice Infestation - Residential","Pest Infestation - Residential", "Chronic Dampness/Mold",
        "Unsatisfactory Living Conditions", 'Carbon Monoxide', "Heat - Excessive Insufficient"
        "Poor Conditions of Property", "Rat Bite", "Rodent Activity", "Squalid Living Conditions"]

    rating = 10
    for item in filtered_data:
        append = False
        if not append:
            for issue in hit_list_5:
                if item['type'] == issue:
                    append=True
                    rating-=0.5
        if not append: 
            for issue in hit_list_1:
                if item['type'] == issue:
                    append=True
                    rating-=1
        if not append:
            for issue in hit_list_3:
                if item['type'] == issue:
                    append=True
                    rating-=3
        if append:
            report.append(item['type'] + " reported at " + item['location_street_name'] + " on " + (item['open_dt'])[:10])

    value ={
        'issues': report,
        'lat': latlong['lat'],
        'lon':latlong['long'],
        'rating': rating
    }
    return value


 




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
    if len(file['features']) == 0:
        return -1

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
   





