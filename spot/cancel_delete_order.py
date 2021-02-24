import json
import aiohttp
import asyncio
import requests
from btseauth_spot import make_headers, BTSE_Endpoint
from utils import get_status_msg
import sys


async def del_order(url, params, headers):
    client = aiohttp.ClientSession()
    try:
        async with client.delete(url, params=params, headers=headers) as response:
            print(await response.text())
            parsed = json.loads(await response.text())
            print(f'\nParsed:\n {parsed}')
            if type(parsed) == list:
                code = parsed[0]['status']
                msg = get_status_msg(code)
                print(f'Status Message: {msg}')
            else:   # error dict returned, get actual error message and return
                msg = parsed['message']
            return msg
    except Exception as e: 
        print(e)
    finally:
        await client.close()

# todo - 2/20/21
# async def cancel_all(pair):
    # get open orders for pair
    # cancel all open orders for pair


async def main():
    
    symbol = 'BTC-USDT' # default or take from command line
    oidlist = ['1741a782-588d-4bf3-8e5a-05f04c760a47'] # default sample
    
    if len(sys.argv[1:]) != 0:
        symbol = sys.argv[1]
        oidlist = []
        oidlist.append(sys.argv[2])
        print(f'\n\nSymbol is: {symbol}, oidlist = {oidlist}')

    path = '/api/v3.2/order'
    url = BTSE_Endpoint+path
    headers = make_headers(path, '')
    
    for oid in oidlist:
        cancel_params = {'orderID': oid, 'symbol': f'{symbol}'}
        msg = await del_order(url=url, params=cancel_params, headers=headers)
        print(f'Returned message: {msg}')

loop = asyncio.get_event_loop()
loop.run_until_complete(main())


'''
sample response:
 {'code': -7006, 'msg': None, 'time': 1604037663859, 'data': None}
 
 valid cancel:
  [{'status': 6, 
  'symbol': 'BTC-USDT', 
  'orderType': 76, 
  'price': 7050.0, 
  'side': 'BUY', 
  'size': 0.002, 
  'orderID': '26ae2091-c0a5-4ef2-8874-ae614876fb38', 
  'timestamp': 1604039550682, 
  'triggerPrice': 0.0, 
  'stopPrice': None, 
  'trigger': False, 
  'message': ''}]

# original REST API
r = requests.delete(
    BTSE_Endpoint+ path,
    params=cancel_params,
    headers=headers
)

print(BTSE_Endpoint + path)
print(cancel_params)
print(r.text)
'''

# cancel_params = {'clOrderID': 'MYOWNORDERID2',
#                  'symbol': 'BTC-USDT'}
# cancel_params = {'orderID': 'b83baf19-7ebe-4997-bfc1-648b06985ad4',
#                 'symbol': 'ETH-USDT'}
# cancel_params = {'orderID': 'f88a5638-8c42-4cf4-aaf1-893acf923038',
#                 'symbol': 'BTC-USDT'}


# client = await self._http_client()
# works on testnet
# print(r.json())

# "clOrderID": "MYOWNORDERID"
# Delete an order
# cancel_params = {'orderID': 'dac5fa04-e419-4054-8fc3-1ed922d595c1', 
#                 'symbol': 'BTC-USD'}

# cancel_params = {'clOrderID': 'MYOWNORDERID', 
#                   'symbol': 'BTC-USD'}





'''
response:
https://testapi.btse.io/spot/api/v3.1/order

{"errorCode":404,"message":"NOTFOUND: 
orderID 00fbfa28-1d32-4801-a926-1af0b88527d4 doesn't exist.",
"status":404}

[{'status': 6, 'symbol': 'BTC-USD', 'orderType': 76,
    'price': 7010.0, 'side': 'BUY', 'size': 0.002,
    'orderID': 'b0f4f063-8a81-41fd-86f6-c8e878ac7454',
    'timestamp': 1601585924998, 'triggerPrice': 0.0, 
    'stopPrice': None, 'trigger': False, 'message': '', 
    'averageFillPrice': 0.0, 'fillSize': 0.0, 'clOrderID': 'MYOWNORDERID', 
    'stealth': 1.0, 'deviation': 1.0}]

'''
'''
success cancel

https://testapi.btse.io/spot/api/v3.1/order
[{"status":6,"symbol":"BTC-USD","orderType":76,"price":7010.0,"side":"BUY","size":0.002,"orderID":"9b96f241-32c3-4610-9a31-553633632db4","timestamp":1601537588875,"triggerPrice":0.0,"stopPrice":null,"trigger":false,"message":"","averageFillPrice":0.0,"fillSize":0.0,"clOrderID":"","stealth":1.0,"deviation":1.0}]

[{'status': 6, 
'symbol': 'BTC-USD', 
'orderType': 76, 
'price': 7010.0, 
'side': 'BUY', 
'size': 0.002, 
'orderID': '9b96f241-32c3-4610-9a31-553633632db4', 
'timestamp': 1601537588875, 
'triggerPrice': 0.0, 
'stopPrice': None, 
'trigger': False,
'message': '', 
'averageFillPrice': 0.0, 
'fillSize': 0.0, 
'clOrderID': '', 
'stealth': 1.0, 
'deviation': 1.0}]

'''