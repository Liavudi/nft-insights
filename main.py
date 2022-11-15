from flask import Flask, render_template

from utils.common import get_mandatory_env_variable
from utils.elastic_search import get_elasticsearch_client
from utils.ether_scan import EtherscanAPIClient

# Connect to etherscan and elastic search
es = get_elasticsearch_client()
eth = EtherscanAPIClient(address="0xb47e3cd837dDF8e4c57F05d70Ab865de6e193BBB", api_key=get_mandatory_env_variable('ETHERSCAN_API_KEY'))
app = Flask(__name__)


def get_gas_fee_for_transaction(block: int):
    pass

def get_eth_price_for_timestamp():
    pass

def get_average_contracts_gas_fee(from_timestamp: float, to_timestamp: float):
    #TODO convert the timestamp to a specific block number
    from_block, to_block = eth.get_blocks_by_timestamp(from_timestamp=from_timestamp, to_timestamp=to_timestamp)
    
    #TODO get log from starting block to ending block
    print(eth.get_logs())
    sum = 0
    blocks =[]
    for block in blocks:
        #TODO convert the gasPrice from the log by multiplying in price of eth in that time
        get_gas_fee_for_transaction(block)

    #TODO sum up all the gas prices at each block and calculate the average fee for this timestamp

print(eth.get_blocks_by_timestamp(from_timestamp="1636984662", to_timestamp="1668520662"))
# print(eth.get_proxy_block_by_number(hex(15975347))['transactions'])

@app.route('/')
def homepage():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
    
