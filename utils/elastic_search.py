from elasticsearch import Elasticsearch, helpers
import json


class ElasticSearchClient:
    ETH_TO_USD_INDEX_NAME = 'eth_to_usd_mapping'

    def __init__(self, cloud_id: str, username: str, password: str) -> None:
        self._client = Elasticsearch(
            cloud_id=cloud_id, http_auth=(username, password))

    def create_index(self, name: str, request_body: dict):
        index_exists = self._client.indices.exists(index=name)
        if index_exists == False:
            self._client.indices.create(index=name, body=request_body)

    def is_timestamp_exists(self, starting_timestamp: int, ending_timestamp: int):
        result = self._client.search(index=self.ETH_TO_USD_INDEX_NAME, query={
            "bool": {
                "filter": [{
                    "range": {
                        "timeStamp": {
                            "gte": f'{starting_timestamp}'
                        }
                    }
                },
                    {
                    "range": {
                        "timeStamp": {
                            "lte": f'{ending_timestamp}'
                        }
                    }
                }
                ]
            }
        }, filter_path=['hits.total.value']).body['hits']['total']['value']
        if result >= 1:
            return True
        return False

    def populate_eth_to_usd_index(self, eth_to_usd_list: list):
        actions = [{
            "_index": self.ETH_TO_USD_INDEX_NAME,
            "_source": {
                "timeStamp": timestamp,
                "price": price
            }
        }
            for timestamp, price in eth_to_usd_list
        ]

        helpers.bulk(self._client, actions)

    def get_eth_price_in_usd(self, timestamp: str):
        result = self._client.search(index=self.ETH_TO_USD_INDEX_NAME, query={
            'bool': {
                'filter': [{
                    'range': {
                        'timeStamp': {
                            'gte': timestamp
                        }
                    }
                }]
            }
        }, filter_path=['hits.hits._source']).body['hits']['hits']

        return result
