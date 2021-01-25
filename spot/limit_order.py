import requests
import json
import aiohttp, asyncio
from decimal import Decimal
from utils import get_status_msg
from btseauth_spot import BTSE_Endpoint, make_headers, get_tracking_nonce

import time 

# this script works on testnet
# uses REST api v3.1

## Place a limit order with price at 7010
'''
limit_order_form = {
  "price": 7050,
  "side": "BUY",
  "size": 0.002,
  "symbol": "BTC-USDT",
  "time_in_force": "GTC",
  "triggerPrice": 0,
  "txType": "LIMIT",
  "type": "LIMIT",
  "clOrderID": "MYOWNORDERID2",
}
'''

limit_order_form = {'symbol': 'BTC-USDT', 'side': 'SELL', 
                    'type': 'LIMIT', 'price': '13318.5', 
                    'size': '0.008000000000000000166533453694', 
                    'triggerPrice': 0, 'time_in_force': 'GTC', 
                    'txType': 'LIMIT', 
                    'clOrderID': 'sell-BTC-USDT-1604346826637811'}
limit_order_form = {'symbol': 'BTC-USD', 'side': 'BUY', 
                    'type': 'LIMIT', 'price': '10418.5', 
                    'size': '0.4980000000000000103667074924', 
                    'triggerPrice': 0, 'time_in_force': 'GTC', 
                    'txType': 'LIMIT', 'clOrderID': 'buy-BTC-USD-1604360430004315'}
limit_order_form = {"symbol": "ETH-USDT", "side": "SELL","type": "LIMIT", 
                    "price": "457.1500000000000253769227854",
                     "size": "0.09800000000000000204003480775",
                      "triggerPrice": 0, "time_in_force": "GTC", 
                      "txType": "LIMIT", 
                      "clOrderID": "sell-ETH-USDT-1604374232705617"}

price = 357.1500000000000253769227854
price = Decimal('%.7g' % price)

limit_order_form = {"symbol": "ETH-USDT", "side": "BUY", "type": "LIMIT",
                     "price": f"{price:f}", 
                     "size": "0.09800000000000000204003480775", 
                     "triggerPrice": 0, "time_in_force": "GTC", 
                     "txType": "LIMIT", "clOrderID": "buy-ETH-USDT-1604374232705551"}


limit_order_form = {"symbol": "BTC-USDT", 
                    "side": "BUY", 
                    "type": "LIMIT", 
                    "price": "18637.8",
                    "size": "0.012", 
                    "triggerPrice": 0,
                    "time_in_force": "GTC", 
                    "txType": "LIMIT", 
                    "clOrderID": "buy-BTC-USDT-1606020895015706"}

limit_order_form = {"symbol": "BTC-USDT", 
                    "side": "BUY", 
                    "type": "LIMIT", 
                    "price": "18637.8",
                    "size": "0.012" }

r_bid_price = 15487.5
r_amount = 0.012

ts = int(time.time())
clientOID = "buy-BTC-USDT-" + str(ts)

limit_order_form = {"symbol": "BTC-USDT",
                    "side": "BUY",
                    "type": "LIMIT",
                    "price": f"{r_bid_price}",
                    "size": f"{r_amount}",
                    "triggerPrice": 0,
                    "time_in_force": "GTC",
                    "txType": "LIMIT",
                    "clOrderID": f"{clientOID}"}

print(limit_order_form)

path = '/api/v3.2/order'
url = BTSE_Endpoint+path

# requests example
'''
def limit_order_r(order_form):
  r = requests.post(
      url,
      json=order_form,
      headers=make_headers(path, json.dumps(order_form))
  )
  print(r.text)
  return r.text
'''

def get_parsed(parsed):
  print(f'\nParsed:\n {parsed}')
  msg = None
  if type(parsed) == list:
      code = parsed[0]['status']
      msg = get_status_msg(code)
      print(f'\nLimit Order Status Message: {msg}')
  else:   # error dict returned, get actual error message and return
      msg = parsed['message']
  return msg

 #  print("RESPONSE from client: " + r + "\n")

# asyncio example
async def limit_order(url, params, headers):
    client = aiohttp.ClientSession()
    try:
      async with client.request('post', url=url, json=params, headers=headers) as response:
        r = await response.json()
        parsed = get_parsed(r)
        print(parsed)
        return r
    except Exception as e:
        print(e)
    finally:
        await client.close()


async def main():
  nonce = get_tracking_nonce()
  print(f'nonce: {nonce}')
  print(f'FULL URL: {url}')
  print(f'limit order form: {limit_order_form}')
  headers=make_headers(path, json.dumps(limit_order_form))
  res = await limit_order(url, params=limit_order_form, headers=headers)


if __name__ == '__main__':
    # limit_order(limit_order_form) # requests version
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())



'''
repsonse: 

nonce:1601499116289

[{"status":2,
"symbol":"BTC-USD",
"orderType":76,
"price":7010.0,
"side":"BUY",
"size":0.002,
"orderID":"9b96f241-32c3-4610-9a31-553633632db4",
"timestamp":1601499117485,
"triggerPrice":0.0,
"stopPrice":null,
"trigger":false,
"message":"",
"averageFillPrice":0.0,
"fillSize":0.0,
"clOrderID":"",
"stealth":1.0,
"deviation":1.0}]

'''
