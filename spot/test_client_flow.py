import json
import aiohttp
import asyncio
import pprint 
from typing import (
    Dict,
)
from btseauth_spot import BTSE_Endpoint, make_headers
from access_methods import BtseEx # get_openorders, limit_order, del_order
from decimal import Decimal
from async_utils import safe_gather
import time

pp = pprint.PrettyPrinter(indent=4)

########################################
#price = 357.1500000000000253769227854
#price = Decimal('%.7g' % price)

ts = int(time.time())
symbol = "BTC-USDT"
clientOID = f"buy-{symbol}-" + str(ts)
price = 1110.5


limit_order_form = {"symbol": f'{symbol}', "side": "BUY", "type": "LIMIT",
                     "price": f"{price:f}", 
                     "size": "0.09800000000000000204003480775", 
                     "triggerPrice": 0, "time_in_force": "GTC", 
                     "txType": "LIMIT", "clOrderID": f'{clientOID}'}
limit_path = 'order'

open_order_params = {'symbol': 'BTC-USDT'}
open_path = 'user/open_orders'

cancel_path = 'order'
cancel_params = {"clOrderID": f'{clientOID}',
                 'symbol':'BTC-USDT'}

params = {'symbol':'BTC-USDT'} 

async def main():
    try:
        be = BtseEx()
        update_trading_rules = await be.update_trading_rules(params=params)
        order_result = await be.open_orders(path=open_path, params=open_order_params)
        limit_result = await be.limit_order(path=limit_path, params=limit_order_form)
        delete_result = await be.delete_order(path=cancel_path, params=cancel_params)
        
        print(f'\n\n ***** delete_result = {delete_result}\n')
        orderID = delete_result[0]['orderID']
        print(f'\n orderID: {orderID}\n')
        # clOrderID = 'buy-BTC-USDT-1606020895015706'
        history = await be.get_trade_history(orderID)

        await be.close_http()
    except Exception as e:
        print(e)    

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

# 0.250-sleep to allow underlying connections to close
loop.run_until_complete(asyncio.sleep(0.250))
loop.close()



