from oauthlib.oauth2 import TokenExpiredError
from requests_oauthlib import OAuth1Session
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv
from base64 import b64encode
from os import getenv
import urllib.parse
import datetime
import requests
import hashlib
import string
import random
import hmac
import json

# source https://stackoverflow.com/questions/55883181/how-can-i-get-all-cities-within-a-given-radius-of-a-given-city-from-the-here-api

load_dotenv()

api_url = "https://revgeocode.search.hereapi.com/v1/revgeocode"


headers = {
    "User-Agent" : "repeaterbookGeoanalysis https://github.com/nicheProgramming/repeaterbookGeoanalysis",
    "Accept": "application/json",
    "Authorization": "OAuth"
}


def create_nonce() -> str:
    length = 6
    letters = string.ascii_letters
    result = "".join(random.choice(letters) for i in range(length))
    
    return result


def authenticate() -> OAuth2Session:
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
    
    if here_session.authorized:
        print("Authenticated to here API successfully")
        return here_session
    else:
        print("Session failed to authenticate, aborting")


def param_formatter(params: dict, prefix: str) -> str:
    loop_iteration = 0
    output = ""
    
    for key, value in params.items():
        loop_iteration += 1
        output += key + "=" + str(value)
        
        if loop_iteration < len(params):
            output += "&"
            
    output = url_encode(output)
    
    return prefix + output


def url_encode(text, safe: str="") -> str:
    if safe == "":
        return urllib.parse.quote(text, safe="") 
    else: 
        return urllib.parse.urlencode(text, safe=safe) 


def handle_http_codes(response: requests.Response) -> bool:
    code = response.status_code
    reason = response.reason
    
    if code >=200 and code <= 299:
        return True
    else:
        print("HTTP Code {0} {1}, request failed. ".format(code, reason))
        exit(1)


def query_api(session: OAuth2Session) -> requests.Response:
    # r for radius here is measured in meters. 
    # 25 miles = 40234 meters
    params = {
        "in": "circle:52.5309,13.3847;r=40234",
        # "apiKey": getenv("here.api.key"),api_url
        "lang": "en-US",
        "types": "city",
        # "limit": 0
    }
    params = url_encode(params, safe=".;:=,")
    request = session.get(api_url, params=params)
    
    print(request.url)
    
    handle_http_codes(request)
    
    r_json = request.json()
    
    return r_json


def get_cities_in_radius(session: OAuth2Session) -> list:
    request = query_api(session)
    
    for item in request["items"]:
        print(json.dumps(item, indent=2))
    
    
    return request


def test_query() -> requests.Response:
    # Not working yet. 403 with good API key. Why?
    url = "https://reverse.geocoder.api.here.com/6.2/reversegeocode.json"

    params = url_encode(params, safe=".,")

    here_session = authenticate()
    
    request = query_api(here_session, url, params)
    
    print(request.content)
    return request