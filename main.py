"""
Module, inccludes script that create an HTML map.
"""
import argparse
from math import radians, cos, sin, asin, sqrt
from geopy.geocoders import Nominatim
import folium

parser = argparse.ArgumentParser(description='HTML-map')
parser.add_argument('year')
parser.add_argument('lat')
parser.add_argument('lon')
parser.add_argument('path')
arg = parser.parse_args()

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees)
    """
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371
    return c * r

def location(path: str, year: str) -> list:
    """
    Function, that parse locations from file.
    """
    years = []
    with open(path, "r", encoding="latin1") as file_info:
        info = file_info.readlines()
    for i in info:
        if str(year) in i:
            years.append(i)
    locations = []
    for i in years:
        locations.append(i.strip().split('\t')[-1])
    return set(locations)


def get_cordinate(data: set) -> list:
    """
    Function, that convert location into coordinates(latitude, longtitude).
    """
    res = []
    geolocator = Nominatim(user_agent="enjdwqniuew")
    for point in data:
        try:
            loc = geolocator.geocode(point)
            if loc:
                res.append((loc.latitude, loc.longitude))
        except Exception:
            continue
    return res


def length_way(user_latitude, user_longtitude, path, year) -> list:
    """ 
    Function, that returns a list of the nearest coordinates to user's point.
    """
    res = []
    for i in get_cordinate(location(path, year)):
        if haversine(user_latitude, user_longtitude,i[0], i[1]) < 1500:
            res.append((i[0], i[1]))
            if len(res) == 10:
                return res
    return res


def get_map(user_latitude, user_longtitude, path, year):
    """
    Function, that create a map and save it to the map.html. 
    """
    map = folium.Map(tiles="Stamen Terrain")
    home = folium.Marker(location=[user_latitude, user_longtitude],\
            icon=folium.Icon(color='blue'))
    map.add_child(home)
    for i in length_way(user_latitude, user_longtitude, path, year):
        loc = folium.Marker(location=[i[0], i[1]],\
            icon=folium.Icon(color='red'))
        map.add_child(loc)
    map.save("map.html")
print(get_map(50.450001, 30.523333, "/Users/lesya/Desktop/UCU IT Projects/Theme 1 (ip, tcp, http, html...)/task2/locations.list", 2000))
if __name__ == '__main__':
    get_map(arg.lat, arg.lon, arg.path, arg.year)
