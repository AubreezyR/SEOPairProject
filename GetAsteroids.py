import requests
import pprint

key = 'gFB2Gf9m63Tcuvvojup15CvLR43k6aKGZEsxCp1Y'

response = requests.get("https://api.nasa.gov/neo/rest/v1/neo/browse?&api_key=" + key)
pprint.pprint(response.json())