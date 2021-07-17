api_key = "AIzaSyDn7OIgopt5Y9ctguL0OVUxCMC7nKadMKQ"
import requests
from urllib.parse import urlencode
data_type = 'json'
endpoint = f"https://maps.googleapis.com/maps/api/geocode/{data_type}"
params = {"address": "1600 Amphitheatre Parkway, Mountain View, CA", "key": api_key}
url_params = urlencode(params)

url = f"{endpoint}?{url_params}"
#print(url)
def extract_lat_lng(address_or_postalcode, data_type = 'json'):
    endpoint = f"https://maps.googleapis.com/maps/api/geocode/{data_type}"
    params = {"address": address_or_postalcode, "key": api_key}
    url_params = urlencode(params)
    url = f"{endpoint}?{url_params}"
    r = requests.get(url)
    if r.status_code not in range(200, 299): 
        return {}
    latlng = {}
    try:
        latlng = r.json()['results'][0]['geometry']['location']
    except:
        pass
    return latlng.get("lat"), latlng.get("lng")

lat, lng = 30.070058, 31.2500699

detail_base_endpoint2 = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
detail_params2 = {
    #"place_id": f"{place_id}",
    "location": f"{lat},{lng}",
    "radius": 100,
    "keyword": "Pharmacies",
    "key": api_key,
    "fields" : "name",
}
detail_params_encoded2 = urlencode(detail_params2)

detail_url2 = f"{detail_base_endpoint2}?{detail_params_encoded2}"

r2 = requests.get(detail_url2)
print(r2.json())