import urllib.request
import json
import urllib.parse
from urllib.parse import urlencode
from urllib.parse import urlparse
from config import MAPQUEST_API_KEY, MBTA_API_KEY

mapbase_url =f'http://www.mapquestapi.com/geocoding/v1/address?'
mbtabase_url = 'https://api-v3.mbta.com/stops?' 

def urlbuild(address):
    """Takes the street address, city and state inputted by the user and builds a URL for the Mapquest API"""
    params = {'key': MAPQUEST_API_KEY , 'location': address }
    addon = urllib.parse.urlencode(params)
    newurl = mapbase_url + addon
    return newurl

def pullmap(customurl):
    """Takes the URL generated above and uses the API to get data about the location"""
    f = urllib.request.urlopen(customurl)
    response_text = f.read().decode('utf-8')
    response_data = json.loads(response_text)
    return response_data

def pullcoords(data):
    """Uses the data pulled by the API to isolate and return the latitude and longitude for the given place"""
    currentcoords =(data['results'][0]['locations'][0]['latLng'])
    return currentcoords['lat'], currentcoords['lng']
    
def mbtaurl(list):
    """Uses the generated coordinated of the location to build a URL for the MBTA API"""
    mbtaparams = {'api_key': MBTA_API_KEY, 'sort': 'distance', 'filter[latitude]': list[0], 'filter[longitude]': list[1]}
    mbtaaddon = urllib.parse.urlencode(mbtaparams)
    mbtacust = mbtabase_url + mbtaaddon
    return mbtacust

def mbta(mbtacustom):
    """Uses the link created above to pull specific info on stops near the location"""
    f = urllib.request.urlopen(mbtacustom)
    response_text = f.read().decode('utf-8')
    response_data = json.loads(response_text)
    return response_data

def mbta_closest(info):
    """Isolates just the closest station from the info pulled from the MBTA API"""
    closeststation = (info['data'][0]['attributes']['name'])
    return closeststation

def mbta_wheel(info):
    """Tells you whether or not the closest station to you is wheelchair accessible or not"""
    accessible = (info['data'][0]['attributes']['wheelchair_boarding'])
    if accessible == 1:
        return 'this station is wheelchair accessible'
    elif accessible == 2:
        return 'this station is unfortunately not wheelchair accessible'
    else:
        return 'it is not known if this station is currently wheelchair accessible'


def main():
    """Goes through and runs everything you need to get the closest station and whether or not it is wheelchair acessible or not"""
    customurl = urlbuild()
    mapinfo = pullmap(customurl)
    coords = pullcoords(mapinfo)
    listcoords = list(coords)
    mbtacustom = mbtaurl(listcoords)
    mbtainfo = mbta(mbtacustom)
    closeststation = mbta_closest(mbtainfo)
    isitaccess = mbta_wheel(mbtainfo)

if __name__ == '__main__':
    main()
