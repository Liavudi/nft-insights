from flask import Flask, render_template


from utils.elastic_search import get_elasticsearch_client
from utils.ether_scan import get_etherscan_client

# Connect to etherscan and elastic search
es = get_elasticsearch_client()
etherscan = get_etherscan_client()
app = Flask(__name__)


@app.route('/')
def homepage():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
    
