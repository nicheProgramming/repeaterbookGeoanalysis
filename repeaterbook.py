import urllib.parse
from time import sleep

import requests
from plot_utils import _convert_FIPS_to_state_name as fips_to_state

RB_API_URL = "https://www.repeaterbook.com/api/export.php"
headers = {
    "User-Agent" : "repeaterbookGeoanalysis \
        https://github.com/nicheProgramming/repeaterbookGeoanalysis",
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
    def __init__(self, json_repeater: dict) -> None:
        self.freq = json_repeater["Frequency"]
        self.in_freq = json_repeater["Input Freq"]
        self.pl_tone = json_repeater["PL"]
        self.tsq = json_repeater["TSQ"]

        self.callsign = json_repeater["Callsign"]
        self.set_emergency_nets(json_repeater)

        self.latitude = float(json_repeater["Lat"])
        self.longitude = float(json_repeater["Long"])
        self.city = json_repeater["Nearest City"]
        self.state_id = {
            json_repeater["State ID"]: ""
        }
        self.state = self.translate_fips()

        self.notes = json_repeater["Notes"]

        self.remove_empty_members()


    def __repr__(self) -> str:
        return self.callsign


    def __lt__(self, other) -> bool:
        return self.callsign < other.callsign


    def remove_empty_members(self) -> None:
        """Deletes empty member variables
        """
        for member in dir(self):
            if not member:
                del member


    def translate_fips(self) -> str:
        """Turn a FIPS United States state ID code into the state's name

        Returns:
            state (str): Name of the state in question
        """
        return list(fips_to_state(self.state_id).keys())[0]


    def set_emergency_nets(self, json_repeater: dict) -> None:
        self.emergency_nets = []

        for net in json_repeater["nets"]:
            if net != "No":
                self.emergency_nets.append(net)


def url_encode(text: str, safe: str="") -> str:
    """Encode text in URL safe manner

    Args:
        text (str): _description_
        safe (str, optional): Characters which should not be encoded. Defaults to "".

    Returns:
        encoded_value (str): Resulting URL safe encoded string
    """
    if not safe:
        return urllib.parse.urlencode(text, safe="")

    return urllib.parse.urlencode(text, safe=safe)


def rq_get(url: str) -> requests.Request:
    """Get request to the Repeaterbook API

    Args:
        url (str): Query URL (with params)

    Returns:
        requests.Request: Resulting request
    """
    return requests.get(url, headers=headers, timeout=60)


# TODO: ensure state is being passed into this func too
def query_rb(city: str) -> dict:
    """ Query Repeaterbook for repeaters in the provided city

    Args:
        city (str): The name of the city you wish to query

    Returns:
        dict: _description_
    """
    query_url = f"{RB_API_URL}?city={city}"

    query = rq_get(query_url)

    wait_seconds = 60

    while "rate_limiting" in query.text:
        print(f"Hit Repeaterbook rate limit. Waiting {wait_seconds} seconds...")

        sleep(60)

        query = rq_get(query_url)

    return query.json()


def categorize_results(query: dict) -> list:
    """Turn repeaterbook output into list of Repeater objects

    Args:
        query (dict): The query results from Repeaterbook

    Returns:
        repeater_list (list): List of rb_repeater objects formed from the Repeaterbook data
    """
    results = query['results']
    output = []

    for repeater in results:
        entry = rb_repeater(repeater)
        output.append(entry)

    return sorted(output)


def query_cities(cities: list) -> list:
    """Query Repeaterbook for each city in the provided list

    Args:
        cities (list): List of cities to query Repeaterbook for

    Returns:
        Amalgam_list (list): List of query_rb output list (list of rb_repeater objects) for all queried cities
    """
    results = []
    seconds = 60

    for city in cities:
        print(f"Querying city {city}...")
        results.append(query_rb(city))
        print(f"Waiting {seconds} seconds before next query...")
        sleep(seconds)

    return results
