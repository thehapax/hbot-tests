#import aiohttp, 
#from utils import get_status_msg
#import sys

import asyncio
from decimal import Decimal
from btseauth_spot import BTSE_Endpoint, make_headers
from utils import get_one_market
import time 
import json
from limit_order import limit_order
from get_market import get_market


path = '/api/v3.2/order'
url = BTSE_Endpoint+path

symbol = 'BTC-USDT'
trading_pair = symbol
params = {'symbol': f'{symbol}'}


def setup_order(params, size, price, side):
    adjusted_price, final_size = get_one_market(params, size, price)
    r_bid_price = adjusted_price
    r_amount = final_size
    print(f'\nAdjusted Price: {r_bid_price}, Final_size: {r_amount}\n\n')
    print('=========================================')

    ts = int(time.time())
    clientOID = "buy-" + symbol + "-" + str(ts)

    limit_order_form = {"symbol": f'{symbol}',
                        "side": f'{side}',
                        "type": "LIMIT",
                        "price": f"{r_bid_price}",
                        "size": f"{r_amount}",
                        "triggerPrice": 0,
                        "time_in_force": "GTC",
                        "txType": "LIMIT",
                        "clOrderID": f"{clientOID}"}
    return limit_order_form


async def get_price(trading_pair, side):
    params = {'symbol': f'{trading_pair}'}
    market = get_market(params)
    mkt_info = market.json()
    #print(mkt_info)
    if side == True:
        price = mkt_info[0]['highestBid']
    elif side == False:
        price = mkt_info[0]['lowestAsk']
    return price


async def execute_order(limit_order_form):
    print(f'limit form: {limit_order_form}')
    headers = make_headers(path, json.dumps(limit_order_form))
    res = await limit_order(url, params=limit_order_form, headers=headers)
    return res


async def main():
        trading_pair = 'BTC-USDT'
        
        print(f'\ntrading pair: {trading_pair}')  
        bid_price: Decimal = await get_price(trading_pair, True)
        ask_price: Decimal = await get_price(trading_pair, False)
        mid_price: Decimal = (bid_price + ask_price) / 2
        print(f'\n bid: {bid_price}, ask : {ask_price}, mid : {mid_price}')
       
        amount: Decimal = Decimal("0.000123456")

        # Intentionally set some prices with too many decimal places s.t. they
        # need to be quantized. Also, place them far away from the mid-price s.t. they won't
        # get filled during the test.
        bid_price = Decimal(mid_price) * Decimal("0.9333192292111341")
        ask_price = Decimal(mid_price) * Decimal("1.0492431474884933")
        print(f'\n Away from mid-price bid: {bid_price}, ask : {ask_price}, mid : {mid_price}\n')

        
        limit_order_form = setup_order(params, amount, bid_price, 'BUY')
        #execute_order(limit_order_form)

        limit_order_form = setup_order(params, amount, ask_price, 'SELL')
        #await execute_order(limit_order_form)

    
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


