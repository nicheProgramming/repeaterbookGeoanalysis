import json
import requests
import urllib.parse

rb_api_url = "https://www.repeaterbook.com/api/export.php"

headers = {
    "User-Agent" : "repeaterbookGeoanalysis https://github.com/nicheProgramming/repeaterbookGeoanalysis",
    "Accept": "application/json"
}

modes = [
    "AllStar",
    "EchoLink",
    "IRLP",
    "Wires",
    "FM Analog",
    "DMR",
    "D-Star",
    "NXDN",
    "APCO P-25",
    "P-25 NAC",
    "M17",
    "Tetra",
    "System Fusion",
    "ATV"
]

bands = {
    "10m": {
        "min": 28,
        "max": 29.7,
        "freq_range": "HF",
        "unit": "MHz"
    },
    "6m": "",
    "2m": "",
    "1.25m": "",
    "70cm": "",
    "33cm": "",
    "23cm": {
        "min": 1.2,
        "max": 1.325,
        "freq_range": "UHF",
        "unit": "GHz"
    }
}


def url_encode(text, safe: str="") -> str:
    if safe == "":
        return urllib.parse.urlencode(text, safe="") 
    else: 
        return urllib.parse.urlencode(text, safe=safe) 
    
    
def build_query(city:str) -> str: 
    query = "?city={}".format(city)
    return rb_api_url + query


def query_rb() -> dict:
    query_url = build_query("Tulsa") 
    q_headers = url_encode(headers)
    
    query = requests.get(query_url, headers=headers)
    
    return query.json()


def categorize_results(query: dict) -> dict:
    results = query['results']
    
    for repeater in results:
        for key, value in repeater.items():
            print(attribute)
        
    return results


results = query_rb()

categorize_results(results)

exit(0)

