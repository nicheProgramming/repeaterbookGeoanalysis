from dotenv import load_dotenv
import requests

load_dotenv()

rb_api_url = "https://www.repeaterbook.com/api"

headers = {
    "User-Agent" : "repeaterbookGeoanalysis https://github.com/nicheProgramming/repeaterbookGeoanalysis",
    "Accept": "application/json"
}


# Get the coordinates of a provided city by name
def get_coords_of_city(city):
    coorts = []
    return coords


# Get a list of cities in a given radius of a location
def get_cities_in_radius(location, radius: int) -> list:
    cities = []
    return cities