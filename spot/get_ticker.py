# get spot market summary, e.g. 
# https://api.btse.com/spot/api/v3.2/market_summary?symbol=BTC-USD

# You can also use wget
#curl -X GET /api.btse.com/spot/api/v3.2/market_summary?symbol=string \
#  -H 'Accept: application/json;charset=UTF-8'

from btseauth_spot import BTSE_Endpoint
import requests
import pprint 
import sys

from typing import (
    List,
    Dict,
    Any,
    Optional,
)

pp = pprint.PrettyPrinter(indent=4)
headers = {
  'Accept': 'application/json;charset=UTF-8'
}

url = BTSE_Endpoint+'/api/v3.2/price'
print(url)

symbol = 'BTC-USDT'
if len(sys.argv[1:]) != 0:
      symbol = sys.argv[1]

r = requests.get(url, params={'symbol': f'{symbol}'}, headers = headers)
pp.pprint(r.json())
print("\n")

res = r.json()
content = res[0]
pp.pprint(content)

print("\n")
symbol = content['symbol']
pp.pprint(symbol)

s = res[0]['symbol']
print(s)
print(type(s))

'''
all_trading_pairs: List[Dict[str, Any]] = r.json()
all_symbols = [item["symbol"] for item in all_trading_pairs]
'''

#print(all_trading_pairs)
#print(all_symbols)

'''
response : 

[   {   'indexPrice': 10760.011089409,
        'lastPrice': 10760.5,
        'markPrice': 0.0,
        'symbol': 'BTC-USDT'}]
        
TICKER =  [{      'indexPrice': 10757.969784007,
                  'lastPrice': 10758.0,
                  'markPrice': 0.0,
                  'symbol': 'BTC-USD'},
            {     'indexPrice': 0.032580719,
                  'lastPrice': 0.041102,
                  'markPrice': 0.0,
                  'symbol': 'ETH-BTC'} ]
        
'''