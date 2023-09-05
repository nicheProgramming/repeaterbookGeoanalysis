import json
import requests
import urllib.parse
from time import sleep
from plot_utils import _convert_FIPS_to_state_name as fips_to_state

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
    "System Fusion"
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

emergency_nets = [
    "ARES",
    "RACES",
    "SKYWARN",
    "CANWARN"
]

class rb_repeater:
    def __init__(self, rb_repeater: dict) -> None:
        self.freq = rb_repeater["Frequency"]
        self.in_freq = rb_repeater["Input Freq"]
        self.pl_tone = rb_repeater["PL"]
        self.tsq = rb_repeater["TSQ"]
        
        self.callsign = rb_repeater["Callsign"]
        self.set_emergency_nets(rb_repeater)
        
        self.latitude = float(rb_repeater["Lat"])
        self.longitude = float(rb_repeater["Long"])
        self.city = rb_repeater["Nearest City"]
        self.state_id = {
            rb_repeater["State ID"]: ""
        }
        self.state = self.translate_fips()
        
        self.notes = rb_repeater["Notes"]
        
        self.remove_empty_members()
       
        
    def __repr__(self) -> str:
        return self.callsign

        
    def __lt__(self, other) -> bool: 
        return self.callsign < other.callsign
    
    
    def remove_empty_members(self) -> None:
        for member in dir(self):
            if member.type() == str and member == "":
                del self.member
            elif member.type() == list and len(member) == 0:
                del self.member
            elif member.type() == int and member == 0:
                del self.member
            elif member.type() == float and member == 0:
                del self.member
            
    
    def translate_fips(self) -> str:
        return list(fips_to_state(self.state_id).keys())[0]
    
    
    def set_emergency_nets(self, rb_repeater: dict) -> None:
        self.emergency_nets = []
        
        for net in emergency_nets:
            if rb_repeater[net] != "No":
                self.emergency_nets.append(net)


def url_encode(text, safe: str="") -> str:
    if safe == "":
        return urllib.parse.urlencode(text, safe="") 
    else: 
        return urllib.parse.urlencode(text, safe=safe) 
    
    
def build_query(city:str) -> str: 
    query = "?city={}".format(city)
    return rb_api_url + query


def query_rb(city: str) -> dict:
    query_url = build_query(city) 
    q_headers = url_encode(headers)
    
    query = requests.get(query_url, headers=headers)
    
    wait_seconds = 60
    
    while "rate_limiting" in query.text:
        print("Hit Repeaterbook rate limit. Waiting {} seconds...".format(wait_seconds))
        
        sleep(60)
        
        query = requests.get(query_url, headers=headers)
    
    return query.json()


def categorize_results(query: dict) -> list:
    results = query['results']
    output = []
    
    for repeater in results:
        entry = rb_repeater(repeater)
        output.append(entry)
        
    return sorted(output)


def query_cities(cities: list) -> list:
    results = []
    seconds = 60
    
    for city in cities:
        print("Querying city {}...".format(city))
        results.append(query_rb(city))
        print("Waiting {} seconds before next query...".format(seconds))
        sleep(seconds)
        
        
    return results
    