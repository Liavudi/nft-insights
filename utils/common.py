import os
import logging
import requests

from typing import List, Tuple


def get_mandatory_env_variable(env_variable_key: str):
    try:
        return os.environ[env_variable_key]
    except:
        error_message = f"Failed to get mandatory enviroment variable {env_variable_key}"
        logging.error(error_message)

        raise RuntimeError(error_message)


def decode_from_hex(input: str):
    return bytes.fromhex(input[2:])[0]


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

    def get_eth_price_in_usd(self, timestamp: str):
        """
        returns the price of the closest eth_price_timestamp before the given timestamp
        """
        for eth_price_timestamp, price in self.eth_to_usd:
            if eth_price_timestamp > timestamp:
                return price
