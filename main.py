from flask import Flask, render_template


from utils.elastic_search import get_elasticsearch_client
from utils.ether_scan import get_etherscan_client

# Connect to etherscan and elastic search
es = get_elasticsearch_client()
eth = get_etherscan_client()
app = Flask(__name__)

# built a skeleton for the implementation
def get_gas_fee_for_transaction(block: int):
    pass

def get_average_contracts_gas_fee(start_timestamp: float, end_timestamp: float):
    #TODO convert the timestamp to a specific block number
    starting_block = eth.get_block_number_by_timestamp(timestamp=start_timestamp, closest="before")
    ending_block = eth.get_block_number_by_timestamp(timestamp=end_timestamp, closest="after")
    #TODO get block number by one time after and one time before
    blocks = []

    #TODO access the each block and take the transaction info
    for block in blocks:
        get_gas_fee_for_transaction(block)

    #TODO sum up all the gas prices at each block and calculate the average fee for this timestamp
print(eth.get_block_number_by_timestamp(timestamp=round(1660741244461 * 1000), closest='before'))
print(eth.get_proxy_block_by_number(hex(15975347))['transactions'])

@app.route('/')
def homepage():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
    
