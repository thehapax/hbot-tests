import requests
import json
import aiohttp, asyncio
from decimal import Decimal
from utils import get_status_msg
from btseauth_spot import BTSE_Endpoint, make_headers, get_tracking_nonce
from get_market import get_a_market
from utils import get_one_market
import time 

# this script works on testnet
# uses REST api v3.1

symbol = 'ETH-USDT'
#d_amount = 0.012
d_amount = 0.000012

r_bid_price = 1733.4234098750984


# adjust size and price for BTSE
params = {'symbol': f'{symbol}'}  
adjusted_price, final_size =  get_a_market(params, d_amount)

r_bid_price = adjusted_price
r_amount = final_size

print(f'\nAdjusted Price: {adjusted_price}, Final_size: {final_size}\n\n')

ts = int(time.time())
clientOID = "buy-" + symbol + "-" + str(ts)

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
  
  #headers=make_headers(path, json.dumps(limit_order_form))
  #res = await limit_order(url, params=limit_order_form, headers=headers)


if __name__ == '__main__':
    # limit_order(limit_order_form) # requests version
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())



'''
sample repsonse: 

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
