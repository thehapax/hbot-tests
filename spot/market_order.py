import socket
import requests
import json
import aiohttp
import asyncio

from utils import get_status_msg
from btseauth_spot import make_headers, BTSE_Endpoint

# works on testnet

'''
 For Market Orders, you will get this errorCode: 400 if you try to use both size and price. 
 So pick one and stick with it. For example, "just the "size" 0.002 btc will do just 
 fine as below, with price commented out. 

 {"errorCode":400,"message":"BADREQUEST: Size and Price should not be mixed","status":400}

'''
## hummingbot does not use market orders, only limit orders?

## Place a market order
mkt_order_form = {
#  "price": 7000,
  "side": "SELL",
  "size": "0.01",
  "symbol": "BTC-USDT",
  "txType": "LIMIT",
  "type": "MARKET"
}

path = '/api/v3.1/order'
url = BTSE_Endpoint+path

def place_mkt_order(mkt_order_form):
    headers = make_headers(path, json.dumps(mkt_order_form))
    r = requests.post(url,
                      json=mkt_order_form,
                      headers=headers)
    print(r.text)


async def market_order(url, params, headers):
    client = aiohttp.ClientSession()
    try:
        response = await client.post(url, json=params, headers=headers)
        r = await response.text()
        print("RESPONSE from client: " + r + "\n")
        parsed = json.loads(await response.text())
        print(f'\nParsed:\n {parsed}')
        if type(parsed) == list:
            code = parsed[0]['status']
            msg = get_status_msg(code)
            print(f'\nLimit Order Status Message: {msg}')
        else:   # error dict returned, get actual error message and return
            msg = parsed['message']
    except Exception as e:
        print(e)
    finally:
        await client.close()

async def main():
    headers = make_headers(path, json.dumps(mkt_order_form))
    res = await market_order(url, params=mkt_order_form,  headers=headers)


if __name__ == "__main__":
#    print("===========\n\n")
#    place_mkt_order(mkt_order_form)
#    print("\n")
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


'''
1: MARKET_UNAVAILABLE = Futures market is unavailable
4: ORDER_FULLY_TRANSACTED = Order is fully transacted
5: ORDER_PARTIALLY_TRANSACTED = Order is partially transacted
6: ORDER_CANCELLED = Order is cancelled successfully
8: INSUFFICIENT_BALANCE = Insufficient balance in account
15: ORDER_REJECTED = Order is rejected
16: ORDER_NOTFOUND = Order is not found with the order ID or clOrderID provided 

sample response:
[{"status":15,
"symbol":"BTC-null",
"orderType":0,
"price":0.0,
"side":"SELL",
"size":0.0,
"orderID":"b2e55bef-495f-4870-97d7-e13d965d979a",
"timestamp":1604025860584,
"triggerPrice":0.0,
"stopPrice":null,
"trigger":false,
"message":""}]

sample:
[{"status":5,
"symbol":"ETH-USDT",
"orderType":77,
"price":405.8198,
"side":"BUY",
"size":0.8116396,
"orderID":"0d68f00b-db4a-4357-9079-0ceea68fedf8",
"timestamp":1604034921121,
"triggerPrice":0.0,
"stopPrice":null,
"trigger":false,
"message":""}]

sample response from requests: 
[{"status":4,
"symbol":"BTC-USD",
"orderType":77,
"price":10758.0,
"side":"BUY",
"size":21.516,
"orderID":"a0fca7aa-f014-4d27-b861-3c950f645bc3",
"timestamp":1601360394360,
"triggerPrice":0.0,
"stopPrice":null,
"trigger":false,
"message":"",
"averageFillPrice":10758.0,
"fillSize":0.002,
"clOrderID":"",
"stealth":1.0,
"deviation":1.0}]
'''