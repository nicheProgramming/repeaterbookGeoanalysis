from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv
from functools import wraps
import repeaterbook
import here

load_dotenv()


def authenticate(func):
    @wraps(func)
    def wrapper():
        # Authenticate to Here
        here_session = here.authenticate()
        func(here_session)
        
    return wrapper


# Get the coordinates of a provided city by name
def get_coords_of_city(city):
    coords = []
    return coords


@authenticate
def main(h_session: OAuth2Session) -> None:
    # Radius in miles
    radius = 10
    
    cities = here.get_cities_in_radius(h_session)
    
    results = repeaterbook.query_cities(cities, radius)

    
    return
    
    
main()