from etherscan import Etherscan

from utils.common import get_mandatory_env_variable


def get_etherscan_client():
    etherscan_api_key = get_mandatory_env_variable('ETHERSCAN_API_KEY')
    return  Etherscan(etherscan_api_key)