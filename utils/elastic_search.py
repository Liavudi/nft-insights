from elasticsearch import Elasticsearch

from utils.common import get_mandatory_env_variable


class ElasticSearchClient:
    def __init__(self, cloud_id: str, username: str, password: str) -> None:
        self._client = Elasticsearch(cloud_id=cloud_id, http_auth=(username, password))

    def create_index(self, name: str, request_body: dict):
        self._client.indices.create(index=name, body=request_body)

    def create_eth_to_usd_index(self):
        request_body = {
            'mappings': {
                'examplecase': {
                    'properties': {
                        'timeStamp': {'index': 'not_analyzed', 'type': 'string'},
                        'ethUsdPrice': {'index': 'not_analyzed', 'type': 'float'},
                    }
                }
            }
        }
        self.create_index(name='eth_to_usd', request_body=request_body)
