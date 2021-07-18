from math import cos, asin, sqrt, pi
import requests
R = 6371

def distance(lat1, lon1, lat2, lon2):
    p = pi / 180
    a = 0.5 - cos((lat2 - lat1) * p) / 2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    return 2 * R * asin(sqrt(a))

def simple_time(lat1, lon1, lat2, lon2, v):
    return int((distance(lat1, lon1, lat2, lon2) / v) * 60)


def clever_time(lat1, lon1, lat2, lon2):
    url = "http://routes.maps.sputnik.ru/osrm/router/viaroute?&loc=" + str(lat1) + "," + str(lon1) + "&loc=" + str(lat2) + "," + str(lon2)
    response = requests.get(url)
    time = (response.json()["route_summary"]["total_time"] + 59) // 60
    return time