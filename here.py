import urllib.parse
from os import getenv
from sys import exit as s_exit

import requests
from dotenv import load_dotenv
from requests_oauthlib import OAuth1Session, OAuth2Session

load_dotenv()

API_URL = "https://revgeocode.search.hereapi.com/v1/revgeocode"

headers = {
    "User-Agent" : "repeaterbookGeoanalysis \
        https://github.com/nicheProgramming/repeaterbookGeoanalysis",
    "Accept": "application/json",
    "Authorization": "OAuth"
}


def authenticate() -> OAuth2Session:
    """Authenticates against the Here API

    Returns:
        OAuth2Session: Authenticated Here API OAuth session
    """
    client_id = getenv("here.client.id")
    key_id = getenv("here.access.key.id")
    key_secret = getenv('here.access.key.secret')
    token_endpoint_url = "https://account.api.here.com/oauth2/token"

    payload = {
       "grant_type": "client_credentials"
    }

    here_session = OAuth1Session(key_id, client_secret=key_secret)
    token = here_session.post(token_endpoint_url, data=payload)
    here_session = OAuth2Session(client_id, token=token.json())

    if not here_session.authorized:
        print("Session failed to authenticate, aborting")

        s_exit(2)

    print("Authenticated to here API successfully")

    return here_session


def url_encode(text: str, safe: str="") -> str:
    """Encodes text to be URL safe

    Args:
        text (str): Text to be encoded
        safe (str, optional): Characters that should not be encoded. Defaults to "".

    Returns:
        encoded_text (str): URL safe text
    """
    if not safe:
        return urllib.parse.quote(text, safe="")

    return urllib.parse.urlencode(text, safe=safe)


def handle_http_codes(response: requests.Response) -> None:
    """Handle request response HTTP codes

    Args:
        response (requests.Response): The HTTP response obj
    """
    code = response.status_code

    if 200 <= code <= 299:
        return True

    reason = response.reason

    print(f"HTTP Code {code} {reason}, request failed. ")

    s_exit(1)


def mi_to_meters(miles: int) -> int:
    """Convert Miles to Meters

    Args:
        miles (int): Miles you wish to convert

    Returns:
        meters (int): Meters result from source miles
    """
    conversion_factor = 1.60934
    kilometers = round(miles * conversion_factor)

    return kilometers * 1000


def meters_to_mi(meters: int) -> int:
    """Convert meters to miles

    Args:
        meters (int): Meters you wish to be converted to miles

    Returns:
        miles (int): Resulting miles
    """
    conversion_factor = 1.60934
    kilometers = meters / 1000

    return round(kilometers / conversion_factor)


def query_api(session: OAuth2Session, radius: int) -> requests.Response:
    """Queries the Here reverse geocode API for a list of cities

    Args:
        session (OAuth2Session): Authenticated Here API OAuth2 session
        radius (int): Radius in miles (converted to meters in function)

    Returns:
        requests.Response: Returns API response for query
    """
    # r for radius here is measured in meters.
    # i.e. 25 miles = 40234 meters
    params = {
        "in": f"circle:36.153980,-95.992775;r={mi_to_meters(radius)}",
        # "apiKey": getenv("here.api.key"),
        "lang": "en-US",
        "types": "city",
        "limit": 100
    }
    params = url_encode(params, safe=".;:=,")
    request = session.get(API_URL, params=params)

    print(request.url)

    handle_http_codes(request)

    return request.json()


# TODO: Sanitize cities on the way out
def get_cities_in_radius(session: OAuth2Session, radius: int) -> list:
    """Get a list of cities in the provided radius. Alert the user if the API limit is hit

    Args:
        session (OAuth2Session): Authenticated Here API OAuth2 session
        radius (int): Radius you wish to be searched in miles

    Returns:
        cities (dict): Dictionary of State Name: City Name
    """
    request = query_api(session, radius)
    num_items_returned =  len(request["items"])
    cities = [item["address"]["city"] for item in request["items"]]

    if num_items_returned == 100:
        print("Warning! Return limit hit when querying here api")
    elif 0 < num_items_returned > 100:
        print(f"Warning! Invalid return count of {num_items_returned}")
    else:
        print(f"Cities found: {num_items_returned}")

    return cities
