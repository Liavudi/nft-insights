import requests
from typing import List, Dict, Tuple
from utils.common import get_mandatory_env_variable
import logging


class EtherscanAPIClient:

    API_URL = 'https://api.etherscan.io/api'

    def __init__(self, address: str, api_key: str):

        self._address = address
        self._api_key = api_key

    def get_blocks_by_timestamp(self, from_timestamp: str, to_timestamp: str) -> Tuple[str, str]:
        try:
            # Get from block
            from_block_response = requests.get(url=self.API_URL,
                                               params={
                                                   'module': 'block',
                                                   'action': 'getblocknobytime',
                                                   'timestamp': from_timestamp,
                                                   'closest': 'after',
                                                   'apiKey': self._api_key
                                               })
            from_block = from_block_response.json()['result']

            # Get to block
            to_block_response = requests.get(url=self.API_URL,
                                             params={
                                                 'module': 'block',
                                                 'action': 'getblocknobytime',
                                                 'timestamp': to_timestamp,
                                                 'closest': 'before',
                                                 'apiKey': self._api_key
                                             })
            to_block = to_block_response.json()['result']

        except Exception as exc:
            logging.error(f'Failed to get blocks by timestamp. exc {exc}')
            raise exc

        return from_block, to_block

    def get_logs(self, contract_address: str, from_block: int, to_block: int) -> List[Dict]:
        try:
            # TODO: support more pages in the future
            transactions_response = requests.get(url=self.API_URL,
                                                 params={
                                                     'module': 'logs',
                                                     'action': 'getLogs',
                                                     'address': contract_address,
                                                     'fromBlock': from_block,
                                                     'toBlock': to_block,
                                                     'page': '1',
                                                     'offset': '1000',
                                                     'apiKey': self._api_key
                                                 })
        except Exception as exc:
            logging.error(f'Failed to get transactions. exc {exc}')
            raise exc

        return transactions_response.json()['result']

    def get_logs_by_timestamp(self, contract_address: str, from_timestamp: str, to_timestamp: str):
        from_block, to_block = self.get_blocks_by_timestamp(
            from_timestamp, to_timestamp)
        return self.get_logs(contract_address=contract_address, from_block=from_block, to_block=to_block)


