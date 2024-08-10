import requests
import CONSTANTS
import json


def getData(api, parameters):
    response = requests.get(f"{api}", params=parameters)
    if response.status_code == 200:
        json_str = response.json()
        formatted_str = json.dumps(json_str, indent=4)
        with open("out.json", "w") as output_file:
            output_file.write(formatted_str)
    else:
        print(response.status_code)


api = "https://api.marketaux.com/v1/news/all?"
params = {
    "api_token": CONSTANTS.marketaux_api_token,
    "symbols": f"RELIANCE.NS",
    "countries": "in",
    "type": "equity",
    "industry": "Energy"
}

getData(api, params)
