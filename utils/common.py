import os
import logging
import requests
import json


from typing import List, Tuple

class jsonDataTest:
    def __init__(self, data) -> None:
        self.data = data    
        self.json_object = json.dumps(self.data, indent=4)
        with open("sample.json", "w") as outfile:
            outfile.write(self.json_object)

def get_mandatory_env_variable(env_variable_key: str):
    try:
        return os.environ[env_variable_key]
    except:
        error_message = f"Failed to get mandatory enviroment variable {env_variable_key}"
        logging.error(error_message)



def calculate_price(input: str):
    return int(input, 0) / 10**18


class StateHelper:
    # Added a hack to keep eth_to_usd in a list instead of elastic search for simplicity (but at cost of performance of course)
    eth_to_usd: List[Tuple[str, float]] = []

    def __init__(self) -> None:
        self.load_eth_to_usd()

    def load_eth_to_usd(self):
        eth_to_usd_response = requests.get(
            'https://www.coingecko.com/price_charts/279/usd/90_days.json')
        eth_to_usd_in_miliseconds = eth_to_usd_response.json()['stats']
        eth_to_usd_in_seconds = []
        for timestamp, price in eth_to_usd_in_miliseconds:
            eth_to_usd_in_seconds.append(
                [
                    int(timestamp / 1000),
                    price
                ]
            )
        self.eth_to_usd = eth_to_usd_in_seconds

    def get_eth_price_in_usd(self, timestamp: str):
        """
        returns the price of the closest eth_price_timestamp before the given timestamp
        """
        price_before = None
        for eth_price_timestamp, price in self.eth_to_usd:
            if eth_price_timestamp < timestamp:
                price_before = price
        if price_before == None:
            raise RuntimeError(
                f'there is no price found for the given timestamp: {timestamp}')
        return price_before
