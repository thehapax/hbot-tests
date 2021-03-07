import requests
import aiohttp
import asyncio
import pprint 
from typing import (
    Dict,
)
from btseauth_spot import BTSE_Endpoint, make_headers
import sys
#from utils import is_json

'''
orderState , string response

ORDER_INSERTED = Order is inserted successfully
ORDER_CANCELLED = Order is cancelled successfully
ORDER_FULLY_TRANSACTED = Order is fully transacted
ORDER_PARTIALLY_TRANSACTED = Order is partially transacted
STATUS_INACTIVE = Order is inactive (could still be on the order books though)
'''

path = '/api/v3.2/user/open_orders'
url = BTSE_Endpoint+path
print(f'url: {url}')

pp = pprint.PrettyPrinter(indent=4)

#symbol = 'BTC-USDT'
#open_order_params = {'symbol': f'{symbol}'}

# Other Examples
# open_order_params = {'symbol': 'BTC-USDT', 'orderID': 'd79e9511-4139-4cae-b020-8309f3658d89'}
# open_order_params = {'clOrderID': 'buy-BTC-USDT-1606020895015706'}
# --> ## open_order_params = {'symbol': 'BTC-USDT', 'clOrderID': 'buy-BTC-USDT-1606020895015706'}


# method to check if orderID = dac5fa04-e419-4054-8fc3-1ed922d595c1 is still an openorder
def get_active_order(id, trade_msg: Dict[str, any]):
    for open_trade in trade_msg:
        if open_trade['orderID'] == id:
            return open_trade

# get all open orderIDs and clOrderIDs
def get_all_order_ids(trade_msg: Dict[str, any]):
    ids = []
    client_ids = []
    for trade in trade_msg:
        id = trade['orderID']
        ids.append(id)
        cid = trade['clOrderID']
        client_ids.append(cid)
    return ids, client_ids

# use these dicts for deletion of open orders
def get_cancelparams(trade_msg: Dict[str, any]): 
    pairs = []
    for trade in trade_msg:
        symbol = trade['symbol']
        oid = trade['orderID']
        info = {'symbol': symbol, 'orderID': oid}
        pairs.append(info)
    return pairs

# get open orders using requests
def get_openorders_r():
    r = requests.get(
        BTSE_Endpoint+ path,
        params=open_order_params,
        headers=make_headers(path, '')
    )
    # all open orders 
    print("\nAll open Orders:")
    pp.pprint(r.json())


async def get_openorders(client, url, params):
    try:
        path = '/api/v3.2/user/open_orders'
        headers = make_headers(path, '')
        async with client.request('get', url=url, params=params, headers=headers) as response:
            result = await response.json()
            # print(result)
            return result
    except Exception as e: 
        print(e)


async def main():
    symbol = 'BTC-USDT' # default or take from command line
    if len(sys.argv[1:]) != 0:
        symbol = sys.argv[1]
        print(f'\n\nSymbol is: {symbol}')
    
    open_order_params = {'symbol': f'{symbol}'}
    print(f'PARAMS: {open_order_params}\n') 

    async with aiohttp.ClientSession() as session:
        response = await get_openorders(client=session, url=url, params=open_order_params)
        print("\n")
        print(f'response: {response}')
        print(f'\nGet parameters from response that are needed for cancelling orders:\n')
        pairs = get_cancelparams(response)
        print(pairs)
        print(f'\nTotal number of pairs: {len(pairs)}\n\n')

        await session.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
    

def get_oids(result):
    # get order ids and client order ids from server result
    oIDs = []
    cIDs = []
    if len(result) == 0:
        # print(type(result))
        print("\nNo Results returned")
        return
    for order in result:
        orderid = order['orderID']
        clOrderID = order['clOrderID']
        #print(f'orderID: {orderid}, clOrderID: {clOrderID}')
        oIDs.append(orderid)
        cIDs.append(clOrderID)

    print(f'\noIDs: {oIDs}')
    print(f'cIDs: {cIDs}')


# get all open orders using async 
async def allinone():
    try:
        symbol = 'ETH-USDT' # default or take from command line
        if len(sys.argv[1:]) != 0:
            symbol = sys.argv[1]
            print(f'\n\nSymbol is: {symbol}')
        
        open_order_params = {'symbol': f'{symbol}'}
        print(f'PARAMS: {open_order_params}\n') 

        path = '/api/v3.2/user/open_orders'
        headers = make_headers(path, '')
        params = open_order_params
        print(f'params: {params}\n')
        print('RESPONSE FROM API:')
        
        async with aiohttp.ClientSession() as client:
            async with client.request('get', url=url, params=params, headers=headers) as response:
                print(f'response: {response}')
                result = await response.json()
                pp.pprint(result)
                get_oids(result)
                
        await client.close()   
    except Exception as e: 
        pass
        #print(e)


#loop = asyncio.get_event_loop()
#loop.run_until_complete(allinone())


# get just this one open order
'''
trade_msg = r.json()
order_id = 'dac5fa04-e419-4054-8fc3-1ed922d595c1'

orderinfo = get_active_order(order_id, trade_msg)
pp.pprint(orderinfo)


EXAMPLE RESPONSE for open orders: 10/10/2020

[   {   'averageFillPrice': 0.0,
        'cancelDuration': 0,
        'clOrderID': 'MYOWNORDERID2',
        'fillSize': 0.0,
        'filledSize': 0.0,
        'orderID': 'cb2d5a05-357d-425a-b965-789d2727fb5a',
        'orderState': 'STATUS_ACTIVE',
        'orderType': 76,
        'orderValue': 14.1,
        'pegPriceDeviation': 0.0,
        'pegPriceMax': 0.0,
        'pegPriceMin': 0.0,
        'price': 7050.0,
        'side': 'BUY',
        'size': 0.002,
        'symbol': 'BTC-USD',
        'timestamp': 1602376422318,
        'trailValue': 0.0,
        'triggerOrder': False,
        'triggerOrderType': 0,
        'triggerOriginalPrice': 0.0,
        'triggerPrice': 0.0,
        'triggerStopPrice': 0.0,
        'triggerTrailingStopDeviation': 0.0,
        'triggered': False},
    {   'averageFillPrice': 0.0,
        'cancelDuration': 0,
        'clOrderID': 'MYOWNORDERID',
        'fillSize': 0.0,
        'filledSize': 0.0,
        'orderID': '4d607bd2-2da3-49ad-b6e7-88cf187386e7',
        'orderState': 'STATUS_ACTIVE',
        'orderType': 76,
        'orderValue': 14.02,
        'pegPriceDeviation': 0.0,
        'pegPriceMax': 0.0,
        'pegPriceMin': 0.0,
        'price': 7010.0,
        'side': 'BUY',
        'size': 0.002,
        'symbol': 'BTC-USD',
        'timestamp': 1602376395636,
        'trailValue': 0.0,
        'triggerOrder': False,
        'triggerOrderType': 0,
        'triggerOriginalPrice': 0.0,
        'triggerPrice': 0.0,
        'triggerStopPrice': 0.0,
        'triggerTrailingStopDeviation': 0.0,
        'triggered': False},
    {   'averageFillPrice': 0.0,
        'cancelDuration': 0,
        'clOrderID': 'MYOWNORDERID',
        'fillSize': 0.0,
        'filledSize': 0.0,
        'orderID': 'dac5fa04-e419-4054-8fc3-1ed922d595c1',
        'orderState': 'STATUS_ACTIVE',
        'orderType': 76,
        'orderValue': 14.02,
        'pegPriceDeviation': 0.0,
        'pegPriceMax': 0.0,
        'pegPriceMin': 0.0,
        'price': 7010.0,
        'side': 'BUY',
        'size': 0.002,
        'symbol': 'BTC-USD',
        'timestamp': 1602376392429,
        'trailValue': 0.0,
        'triggerOrder': False,
        'triggerOrderType': 0,
        'triggerOriginalPrice': 0.0,
        'triggerPrice': 0.0,
        'triggerStopPrice': 0.0,
        'triggerTrailingStopDeviation': 0.0,
        'triggered': False}]
'''

### old errors
    #    this line below causes 'FORBIDDEN: Signature is incorrect'
    #    headers = make_headers(path, json.dumps(open_order_params))
    # ----- 
    #    this line below causes TypeError: can only concatenate str (not "dict") to str
    #    headers = make_headers(path, open_order_params)
