import requests
import json
api_key = '55ibuj2HAmeDpBPCUHWOgQgGBC96DHwj4RRkO2GC'
url = "https://api.nasa.gov/neo/rest/v1/feed?start_date=2015-09-07&end_date=2015-09-14&"
response = requests.get(url + "api_key=" + api_key)
print(response.json()['near_earth_objects']['2015-09-11'][0]['close_approach_data'][0]['relative_velocity'])
#0 = date 2

#name, absolute_magnitude_h,
def create_databse:
    
}