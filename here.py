import requests

here_api_url = "https://reverse.geocoder.api.here.com/6.2/reversegeocode.json?"
here_api_params = {
    "prox": "",
    "app_id": "",
    "app_code": "",
    "mode": "",
    "level": "",
    "gen": 9
}

# source https://stackoverflow.com/questions/55883181/how-can-i-get-all-cities-within-a-given-radius-of-a-given-city-from-the-here-api