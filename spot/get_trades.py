import requests
from btseauth_spot import BTSE_Endpoint, make_headers
import pprint
from decimal import Decimal

# public orders placed for specific symbol
# this is a public endpoint

pp = pprint.PrettyPrinter(indent=4)

BTSE_Endpoint = 'https://testapi.btse.io/spot'
headers = {
  'Accept': 'application/json;charset=UTF-8'
}
path = '/api/v3.2/trades'
params={'symbol': 'BTC-USDT'}
r = requests.get(BTSE_Endpoint+path,
                params=params,
                headers=headers)
print(r.text)

print("\n")
#print(r.json())


'''
Example response: 

[{'price': 10758.0, 'size': 0.001, 'side': 'SELL', 'symbol': 'BTC-USD', 'serialId': 111137017, 'timestamp': 1602251507000}, 
{'price': 10757.5, 'size': 0.001, 'side': 'BUY', 'symbol': 'BTC-USD', 'serialId': 111136991, 'timestamp': 1602251352000}, 
{'price': 10741.5, 'size': 0.001, 'side': 'BUY', 'symbol': 'BTC-USD', 'serialId': 111136897, 'timestamp': 1602251099000}, 
{'price': 10757.5, 'size': 0.001, 'side': 'BUY', 'symbol': 'BTC-USD', 'serialId': 111136847, 'timestamp': 1602250926000}, 
{'price': 10758.0, 'size': 0.4, 'side': 'SELL', 'symbol': 'BTC-USD', 'serialId': 111131641, 'timestamp': 1602234996000}, 
{'price': 10753.0, 'size': 0.003, 'side': 'BUY', 'symbol': 'BTC-USD', 'serialId': 111131325, 'timestamp': 1602234015000}, 
{'price': 10758.0, 'size': 0.001, 'side': 'SELL', 'symbol': 'BTC-USD', 'serialId': 111130532, 'timestamp': 1602231555000}, 
{'price': 10757.5, 'size': 0.001, 'side': 'BUY', 'symbol': 'BTC-USD', 'serialId': 111130274, 'timestamp': 1602230590000}, 
{'price': 10757.5, 'size': 0.001, 'side': 'BUY', 'symbol': 'BTC-USD', 'serialId': 111129999, 'timestamp': 1602230276000}, 
{'price': 10757.5, 'size': 0.001, 'side': 'BUY', 'symbol': 'BTC-USD', 'serialId': 111129979, 'timestamp': 1602230250000}]

'''