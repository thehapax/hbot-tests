import requests
from btseauth_spot import BTSE_Endpoint, make_headers
import pprint
from decimal import Decimal
import time

'''
get_my_tradehistory fetches 
Already closed Orders, that have been fully transacted
based on OrderID, client order ID and timestamp (startTime) params

> must use startTime in order to filter appropriately, or too much data returned
> Use a 13 digit timestamp

Sample Returned Data: 
            
    [   {   'base': 'BTC',
        'clOrderID': None,
        'feeAmount': 2e-06,
        'feeCurrency': 'BTC',
        'filledPrice': 10758.0,
        'filledSize': 0.002,
        'orderId': 'b3a65f8e-e838-4c13-adf4-62fef98504a1',
        'orderType': 77,
        'price': 21.516,
        'quote': 'USD',
        'realizedPnl': 0.0,
        'serialId': 110947333,
        'side': 'BUY',
        'size': 21.516,
        'symbol': 'BTC-USD',
        'timestamp': 1601791330000,
        'total': 0.0,
        'tradeId': '1c062ffa-0386-4d63-8cff-c6f4de05a270',
        'triggerPrice': 0.0,
        'triggerType': 0,
        'username': 'hapax10test',
        'wallet': 'SPOT@'},
    ]

'''

_last_tracking_nonce_low_res = 0

# use this method to help generate startTime
def get_tracking_nonce_low_res() -> int:
    global _last_tracking_nonce_low_res
    nonce = int(time.time() * 1e3)
    _last_tracking_nonce_low_res = nonce if nonce > _last_tracking_nonce_low_res else _last_tracking_nonce_low_res + 1
    return _last_tracking_nonce_low_res



pp = pprint.PrettyPrinter(indent=4)
path = '/api/v3.2/user/trade_history'

# params = {}
# params = { 'tradeId' : '68c86d7a-502c-4400-ad3b-02ef3474937b' } # currently this filters does not work on BTSE Spot API 

params = {'symbol': 'BTC-USDT', 
         'orderId': '7bda5bcc-68fb-459e-8376-bcd8137600c9',
          'startTime': 1611040430000}

params = { 'orderID': 'a01416b4-96b7-429e-8ed4-33ee8bf06d0a', # this works
         'startTime': 1606469000000 } 

# params = {'clOrderID': 'buy-BTC-USDT-1606020895015706'} # this works - when testing, don't create a single client Order ID for multiple orders

print(f'Params: {params}')

fullpath = BTSE_Endpoint+path
print(f'REST API: {fullpath}')

r = requests.get(fullpath,
                params=params,
                headers=make_headers(path, ''))

result = r.json()
pp.pprint(result)

