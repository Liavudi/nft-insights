from flask import Flask, render_template

from utils.common import get_mandatory_env_variable, decode_from_hex, StateHelper
from utils.elastic_search import ElasticSearchClient
from utils.ether_scan import EtherscanAPIClient

# Connect to etherscan and elastic search
es_client = ElasticSearchClient(username=get_mandatory_env_variable('ELASTIC_USERNAME'),
                                password=get_mandatory_env_variable(
                                    'ELASTIC_PASSWORD'),
                                cloud_id="elastic:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvJDllMDg2NzdiMDkzMjRmMGJiMzY2MDBmYWFhYTAwZDNiJGExMjVmNWU4N2ZlNTRjZTBhYzcwNWQ4YTQ4YTU3NmM0")
eth_client = EtherscanAPIClient(
    api_key=get_mandatory_env_variable('ETHERSCAN_API_KEY'))

state_helper = StateHelper()
app = Flask(__name__)


def get_average_contracts_gas_fee(contract_address: str, from_timestamp: float, to_timestamp: float):
    # TODO convert the timestamp to a specific block number
    from_block, to_block = eth_client.get_blocks_by_timestamp(
        from_timestamp=from_timestamp, to_timestamp=to_timestamp)

    # TODO get log from starting block to ending block
    transaction_logs = eth_client.get_logs(
        contract_address=contract_address, from_block=from_block, to_block=to_block)
    sum = 0
    for transaction_log in transaction_logs:
        # TODO convert the gasPrice from the log by multiplying in price of eth in that time
        gas_price_in_eth = decode_from_hex(transaction_log['gasPrice'])
        eth_in_usd = state_helper.get_eth_price_in_usd(
            timestamp=decode_from_hex(transaction_log['timeStamp']))
        sum += eth_in_usd * gas_price_in_eth

    average_price = sum / len(transaction_log)
    return average_price


# def calculate_contract_average_gas_fee(contract_name: str, contract_address: str, days_ago: int = 90):
#     from_timestamp = get_timestamp_in_seconds(days_ago=days_ago)
#     get_average_contracts_gas_fee(contract_address=contract_address, from_timestamp=from_timestamp, to_timestamp=to_timestamp)

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/contract-average-gas-fee')
def contract_average_gas_fee():
    return render_template('index.html')


if __name__ == '__main__':
    # es_client.create_eth_to_usd_index()
    # es_client.populate_eth_to_usd_index()
    contracts = ['0xb47e3cd837dDF8e4c57F05d70Ab865de6e193BBB', '0x60e4d786628fea6478f785a6d7e704777c86a7c6']

    app.run(debug=True)
