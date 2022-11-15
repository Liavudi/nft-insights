from elasticsearch import Elasticsearch

from utils.common import get_mandatory_env_variable


def get_elasticsearch_client():
    """
    Get a connection to elastic search
    """
    elastic_username = get_mandatory_env_variable('ELASTIC_USERNAME')
    elastic_password = get_mandatory_env_variable('ELASTIC_PASSWORD')
    return Elasticsearch(cloud_id="elastic:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvJDllMDg2NzdiMDkzMjRmMGJiMzY2MDBmYWFhYTAwZDNiJGExMjVmNWU4N2ZlNTRjZTBhYzcwNWQ4YTQ4YTU3NmM0",
                         http_auth=(elastic_username, elastic_password))
