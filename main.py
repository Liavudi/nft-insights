from flask import Flask, render_template, request
import json

from utils.common import get_mandatory_env_variable, calculate_price, StateHelper, jsonDataTest
from utils.elastic_search import ElasticSearchClient
from utils.ether_scan import EtherscanAPIClient


# Connect to etherscan and elastic search
es_client = ElasticSearchClient(username=get_mandatory_env_variable('ELASTIC_USERNAME'),
                                password=get_mandatory_env_variable(
                                    'ELASTIC_PASSWORD'),
                                cloud_id=get_mandatory_env_variable(
                                    'ELASTIC_CLOUD_ID')
                                )
eth_client = EtherscanAPIClient(
    api_key=get_mandatory_env_variable('ETHERSCAN_API_KEY'))

state_helper = StateHelper()
app = Flask(__name__)


def get_average_contracts_gas_fee(contract_address: str, from_timestamp: float, to_timestamp: float):
    from_block, to_block = eth_client.get_blocks_by_timestamp(
        from_timestamp=from_timestamp, to_timestamp=to_timestamp)

    transaction_logs = eth_client.get_logs(
        contract_address=contract_address, from_block=from_block, to_block=to_block)
    sum = 0
    if len(transaction_logs) > 0:
        for transaction_log in transaction_logs:
            gas_price_in_eth = calculate_price(transaction_log['gasPrice'])
            eth_in_usd_in_the_transaction_time = state_helper.get_eth_price_in_usd(
                timestamp=int(transaction_log['timeStamp'], 0))
            sum += eth_in_usd_in_the_transaction_time * gas_price_in_eth

        average_price = sum / len(transaction_logs)
        return average_price
    


def populate_one_day_to_elastic(contract_address: str, starting_timestamp: int):
    one_hour = 3600
    eth_to_usd_list = []
    hours = 3      
    for i in range(hours):
        eth_to_usd_list.append(
            [f"{starting_timestamp}", f"{get_average_contracts_gas_fee(contract_address, starting_timestamp, starting_timestamp + one_hour)}"])
        starting_timestamp += one_hour
    parsed_list = []
    for i in eth_to_usd_list:
        if i[1] != 'None':
            parsed_list.append(i)    
    es_client.populate_eth_to_usd_index(parsed_list)

populate_one_day_to_elastic('0xb47e3cd837dDF8e4c57F05d70Ab865de6e193BBB', 1665018000 )

@app.route('/')
def homepage():
    data = es_client.get_eth_price_in_usd()
    return render_template('index.html', chart_data=data)


@app.route('/contract-average-gas-fee', methods=['GET'])
def contract_average_gas_fee():
    return ''

if __name__ == '__main__':
    contracts = ['0xb47e3cd837dDF8e4c57F05d70Ab865de6e193BBB',
                 '0x60e4d786628fea6478f785a6d7e704777c86a7c6']

    app.run(debug=True)
