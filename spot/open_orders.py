import requests
import aiohttp
import asyncio
import pprint 
from typing import (
    Dict,
)
from btseauth_spot import BTSE_Endpoint, make_headers
from utils import is_json

# import json


'''
orderState , string

ORDER_INSERTED = Order is inserted successfully
ORDER_CANCELLED = Order is cancelled successfully
ORDER_FULLY_TRANSACTED = Order is fully transacted
ORDER_PARTIALLY_TRANSACTED = Order is partially transacted
STATUS_INACTIVE = Order is inactive (could still be on the order books though)

'''

pp = pprint.PrettyPrinter(indent=4)
#open_order_params = {'symbol': 'ETH-USDT'}
open_order_params = {'symbol': 'BTC-USDT'}
# open_order_params = {'symbol': 'BTC-USDT', 'orderID': ['d79e9511-4139-4cae-b020-8309f3658d89', 'f88a5638-8c42-4cf4-aaf1-893acf923038']}
# open_order_params = {'symbol': 'BTC-USDT', 'orderID': 'd79e9511-4139-4cae-b020-8309f3658d89'}
# open_order_params = {'symbol': 'BTC-USDT', 'orderID': ['f88a5638-8c42-4cf4-aaf1-893acf923038']}
# open_order_params = {'symbol': 'BTC-USDT', 'orderID': ['d79e9511-4139-4cae-b020-8309f3658d89']}

open_order_params = {'symbol': 'BTC-USDT', 'clOrderID': 'buy-BTC-USDT-1606020895015706'}
#open_order_params = {'clOrderID': 'buy-BTC-USDT-1606020895015706'}

#open_order_params = {'clOrderID': 'buy-BTC-USDT-1606020895015706'}
#open_order_params = {'symbol': 'BTC-USDT'}


path = '/api/v3.2/user/open_orders'
url = BTSE_Endpoint+path
print(f'url: {url}')


# method to check if orderID = dac5fa04-e419-4054-8fc3-1ed922d595c1 is still an openorder
def get_active_order(id, trade_msg: Dict[str, any]):
    for open_trade in trade_msg:
        if open_trade['orderID'] == id:
            return open_trade

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

def get_openorders_r():
    # get open orders using requests
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
    # this causes 'FORBIDDEN: Signature is incorrect'
    #    headers = make_headers(path, json.dumps(open_order_params))
    # ----- 
    # this causes TypeError: can only concatenate str (not "dict") to str
    #    headers = make_headers(path, open_order_params)

    print(f'PARAMS: {open_order_params}\n') 
    #client = aiohttp.ClientSession()

    async with aiohttp.ClientSession() as session:
        response = await get_openorders(client=session, url=url, params=open_order_params)
        print("\n")
        pairs = get_cancelparams(response)
        print(f'Total number of pairs: {len(pairs)}\n\n')
        print(pairs)
        await session.close()

#loop = asyncio.get_event_loop()
#loop.run_until_complete(main())
    

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


async def allinone():
    try:
        path = '/api/v3.2/user/open_orders'
        headers = make_headers(path, '')
        params = open_order_params
        print(f'params: {params}\n')
        print('RESPONSE FROM API:')
        
        async with aiohttp.ClientSession() as client:
            async with client.request('get', url=url, params=params, headers=headers) as response:
                result = await response.json()
                pp.pprint(result)
                get_oids(result)
                
        await client.close()   
    except Exception as e: 
        print(e)

loop = asyncio.get_event_loop()
loop.run_until_complete(allinone())


#order_ids, client_ids = get_all_order_ids(response)
#print(f'Order IDs: {order_ids} \n\nClient IDs: {client_ids}\n')


#        async with client.get(url, params=params, headers=headers) as response:
            # print(await response.text())
#            parsed = json.loads(result)
#            pp.pprint("\nParsed:")
#            pp.pprint(parsed)


''' what was this used for? 
try:
    if is_json(r.text):
        res = r.json()
        dres = res[0]
        print(dres.get('symbol'))
        pp.pprint(dres)
except IndexError as e:
    print(r.text)
'''


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



'''
python3 open_orders.py 

https://testapi.btse.io/spot/api/v3.1/user/open_orders

[{"orderType":76,
"price":7010.0,
"size":0.002,
"side":"BUY",
"orderValue":14.02,
"filledSize":0.0,
"pegPriceMin":0.0,
"pegPriceMax":0.0,
"pegPriceDeviation":0.0,
"cancelDuration":0,
"timestamp":1600930554219,
"orderID":"11edaa79-7f16-4526-a5d6-d59134072a56",
"triggerOrder":false,
"triggerPrice":0.0,
"triggerOriginalPrice":0.0,
"triggerOrderType":0,
"triggerTrailingStopDeviation":0.0,
"triggerStopPrice":0.0,
"symbol":"BTC-USD",
"trailValue":0.0,
"averageFillPrice":0.0,
"fillSize":0.0,
"clOrderID":null,
"orderState":"STATUS_ACTIVE",
"triggered":false}]

'''
