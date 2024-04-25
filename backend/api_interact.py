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
    url = 'https://data.boston.gov/api/3/action/datastore_search_sql?sql=SELECT%20*%20from%20%22e6013a93-1321-4f2a-bf91-8d8a02f1e62f%22%20WHERE%20%22longitude%22%20BETWEEN%20%27' + lon1 + '%27%20AND%20%27' + lon2 + '%27'
    response = requests.get(url)
    data = response.json()
    filtered_data = []
    for item in data['result']['records']:
        if item['latitude'] < lat1 and item['latitude'] > lat2:
            filtered_data.append(item)
    
    report = []
    # Rankings: 
    # -0.25 : "Aircraft Noise Disturbance", "Animal Noise Disturbances", "Automotive Noise Disturbance", 
    #'Dumpster & Loading Noise Disturbances', "Loud Parties/Music/People", "Undefined Noise Disturbance", "Unshoveled Sidewalk"
    # -0.5 "Improper Storage of Trash (Barrels)", "No Utilities Residential - Gas", "No Utilities Residential - Electricity",
    # "No Utilities Residential - Water", "Student Move-in Issues", "Student Overcrowding", "Unsatisfactory Utilities - Electrical Plumbing"
    # -2 "Bed Bugs", "Mice Infestation - Residential","Pest Infestation - Residential", "Chronic Dampness/Mold",
        #"Unsatisfactory Living Conditions", 'Carbon Monoxide', "Heat - Excessive Insufficient"
        #"Poor Conditions of Property", "Rat Bite", "Rodent Activity", "Squalid Living Conditions"
    hit_list_25 = ["Aircraft Noise Disturbance", "Animal Noise Disturbances", "Automotive Noise Disturbance", 
                   'Dumpster & Loading Noise Disturbances', "Loud Parties/Music/People", "Undefined Noise Disturbance", "Unshoveled Sidewalk"]
    hit_list_5 = ["Improper Storage of Trash (Barrels)", "No Utilities Residential - Gas", "No Utilities Residential - Electricity",
                   "No Utilities Residential - Water", "Student Move-in Issues", "Student Overcrowding", "Unsatisfactory Utilities - Electrical Plumbing"]
    hit_list_1 = [ "Bed Bugs", "Mice Infestation - Residential","Pest Infestation - Residential", "Chronic Dampness/Mold",
        "Unsatisfactory Living Conditions", 'Carbon Monoxide', "Heat - Excessive Insufficient"
        "Poor Conditions of Property", "Rat Bite", "Rodent Activity", "Squalid Living Conditions"]
    hit_list = ["Aircraft Noise Disturbance", "Animal Noise Disturbances", "Automotive Noise Disturbance", 
                "Bed Bugs", "Mice Infestation - Residential","Pest Infestation - Residential", "Chronic Dampness/Mold",
                  "Unsatisfactory Living Conditions", 'Carbon Monoxide', 'Dumpster & Loading Noise Disturbances',
                  "Heat - Excessive Insufficient", "Improper Storage of Trash (Barrels)", "Lead", "Loud Parties/Music/People",
                  "No Utilities Residential - Gas", "No Utilities Residential - Electricity", "No Utilities Residential - Water",
                  "Poor Conditions of Property", "Rat Bite", "Rodent Activity", "Squalid Living Conditions", "Student Move-in Issues",
                  "Student Overcrowding", "Undefined Noise Disturbance", "Unsatisfactory Utilities - Electrical Plumbing", 
                  "Unshoveled Sidewalk"
                ]
    rating = 10
    for item in filtered_data:
        append = False
        if not append:
            for issue in hit_list_25:
                if item['type'] == issue:
                    append=True
                    rating=-0.25
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
        if append:
            report.append(item['type'] + " reported at " + item['location_street_name'] )

    print(report, rating)
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
   





