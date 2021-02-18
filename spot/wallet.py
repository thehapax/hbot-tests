import socket
import requests
import json
from btseauth_spot import make_headers, BTSE_Endpoint
import pprint
from decimal import Decimal

pp = pprint.PrettyPrinter(indent=4)
#path = '/api/v2/user/wallet_history'

path = '/api/v3.2/user/wallet'
btse_test_url ='https://testapi.btse.io/spot/api/v3.2/user/wallet'

#params ={}
params = {'currency': 'BTC'} 
# params don't work, all balances are returned. 
# await self._api_request("get", "price?symbol=BTC-USDT")

headers=make_headers(path, '')

print(f'headers: {headers}')
print(f'params: {params}')
print(f'url: {btse_test_url}')

r = requests.get(
    btse_test_url,
    params=params,
    headers=headers)

print(str(r))
print(str(r.text))

response = r.json()
pp.pprint(response)

'''
for coin in response:
    if str(coin['available']) != '0.0':
        print(str(coin['currency']))
        avail = Decimal(str(coin['available']))
        total = Decimal(str(coin['total']))
        print("\tAvail: " + str(avail))
        print("\tTotal: " + str(total))
'''

        


'''
sample response:  - returns balances of all wallets, selective params don't seem to make a difference

nonce:1601362910720
<Response [200]>

[{'currency': 'USD', 'total': 9773.219, 'available': 9759.199}, 
{'currency': 'EUR', 'total': 8000.0, 'available': 8000.0}, 
{'currency': 'GBP', 'total': 7500.0, 'available': 7500.0}, 
{'currency': 'HKD', 'total': 70000.0, 'available': 70000.0},
 {'currency': 'SGD', 'total': 13000.0, 'available': 13000.0}, 
 {'currency': 'MYR', 'total': 0.0, 'available': 0.0}, 
 {'currency': 'CNY', 'total': 0.0, 'available': 0.0},
  {'currency': 'IDR', 'total': 0.0, 'available': 0.0}, 
  {'currency': 'THB', 'total': 0.0, 'available': 0.0}, 
  {'currency': 'JPY', 'total': 0.0, 'available': 0.0}, 
  {'currency': 'AUD', 'total': 0.0, 'available': 0.0}, 
  {'currency': 'AED', 'total': 0.0, 'available': 0.0}, 
  {'currency': 'CAD', 'total': 0.0, 'available': 0.0}, 
  {'currency': 'VND', 'total': 0.0, 'available': 0.0}, 
  {'currency': 'INR', 'total': 0.0, 'available': 0.0}, 
  {'currency': 'PHP', 'total': 0.0, 'available': 0.0}, 
  {'currency': 'CHF', 'total': 0.0, 'available': 0.0},
  {'currency': 'USDT', 'total': 10000.0, 'available': 10000.0},
   {'currency': 'BTC', 'total': 15.605787, 'available': 15.605787}, 
   {'currency': 'ETH', 'total': 70.0, 'available': 70.0}, 
   {'currency': 'LTC', 'total': 100.0, 'available': 100.0}, 
   {'currency': 'TUSD', 'total': 50000.0, 'available': 50000.0}, 
   {'currency': 'USDC', 'total': 50181.767675, 'available': 50181.767675},
    {'currency': 'FEE', 'total': 0.0, 'available': 0.0}, 
    {'currency': 'BNS', 'total': 0.0, 'available': 0.0}, 
    {'currency': 'XMR', 'total': 0.0, 'available': 0.0}, 
    {'currency': 'DC', 'total': 0.0, 'available': 0.0}, 
    {'currency': 'BTSE', 'total': 0.0, 'available': 0.0},
     {'currency': 'XAUT', 'total': 0.0, 'available': 0.0}, 
     {'currency': 'BCB', 'total': 0.0, 'available': 0.0}, 
     {'currency': 'XRP', 'total': 0.0, 'available': 0.0},
      {'currency': 'TR_USDT', 'total': 0.0, 'available': 0.0},
       {'currency': 'TRYB', 'total': 0.0, 'available': 0.0}, 
       {'currency': 'LEO', 'total': 0.0, 'available': 0.0}, 
       {'currency': 'TRX', 'total': 0.0, 'available': 0.0},
        {'currency': 'STAKE', 'total': 0.0, 'available': 0.0}, 
        {'currency': 'PHNX', 'total': 0.0, 'available': 0.0}, 
        {'currency': 'FRM', 'total': 0.0, 'available': 0.0}, 
        {'currency': 'HXRO', 'total': 0.0, 'available': 0.0},
         {'currency': 'NZD', 'total': 0.0, 'available': 0.0},
          {'currency': 'RUB', 'total': 0.0, 'available': 0.0}, 
          {'currency': 'ZAR', 'total': 0.0, 'available': 0.0}, 
          {'currency': 'UNI', 'total': 0.0, 'available': 0.0}, 
          {'currency': 'CRV', 'total': 0.0, 'available': 0.0}, 
          {'currency': 'COMP', 'total': 0.0, 'available': 0.0}, 
          {'currency': 'SWRV', 'total': 0.0, 'available': 0.0}, 
          {'currency': 'BRZ', 'total': 0.0, 'available': 0.0}]

'''