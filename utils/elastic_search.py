import json
import requests

from elasticsearch import Elasticsearch


class ElasticSearchClient:
    ETH_TO_USD_INDEX_NAME = 'eth_to_usd_mapping'

    def __init__(self, cloud_id: str, username: str, password: str) -> None:
        self._client = Elasticsearch(
            cloud_id=cloud_id, http_auth=(username, password))

    def create_index(self, name: str, request_body: dict):
        index_exists = self._client.indices.exists(index=name)
        if index_exists == False:
            self._client.indices.create(index=name, body=request_body)

    def create_eth_to_usd_index(self):
        request_body = {
            'mappings': {
                'properties': {
                    'timeStamp': {'type': 'text'},
                    'price': {'type': 'float'}
                }
            }
        }
        self.create_index(self.ETH_TO_USD_INDEX_NAME,
                          request_body=request_body)

    def populate_eth_to_usd_index(self):
        eth_to_usd_response = requests.get('https://www.coingecko.com/price_charts/279/usd/90_days.json')
        parsed_eth_to_usd_list = eth_to_usd_response.json()['stats']
        bulk_list = []
        for eth_to_usd_timestamp, eth_to_usd_price in parsed_eth_to_usd_list:
            action = json.dumps({
                'index': {
                    '_index': self.ETH_TO_USD_INDEX_NAME,
                    '_id': int(eth_to_usd_timestamp),
                    'type': 'text'
                }
            })
            item = json.dumps({
                "timeStamp": eth_to_usd_timestamp,
                "price": eth_to_usd_price
            })
            bulk_list.append(action)
            bulk_list.append(item)
        #TODO need to solve this, it is not working, receiving bad request need to tweak the request to make it work
        self._client.bulk(index=self.ETH_TO_USD_INDEX_NAME,
                          operations=item)

    def get_eth_price_in_usd(self, timestamp: str):
        result = self._client.search(index=self.ETH_TO_USD_INDEX_NAME, query={
            'bool': {
                'filter': [{
                    'range': {
                        'timeStamp': {
                            'lte': timestamp
                        }
                    }
                }]
            }
        }, size=1, filter_path=['hits.max_score'])
        print(result)
