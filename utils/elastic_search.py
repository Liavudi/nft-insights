import requests

from elasticsearch import Elasticsearch

from utils.common import get_mandatory_env_variable


class ElasticSearchClient:
    def __init__(self, cloud_id: str, username: str, password: str) -> None:
        self._client = Elasticsearch(cloud_id=cloud_id, http_auth=(username, password))

    def create_index(self, name: str, request_body: dict):
        self._client.indices.create(index=name, body=request_body)

    def create_eth_to_usd_index(self):
        eth_to_usd_response = requests.get('https://www.coingecko.com/price_charts/279/usd/90_days.json')
        parsed_eth_to_usd_list = eth_to_usd_response.json()['stats']
        self.index(index='eth_to_usd', document=parsed_eth_to_usd_list)
