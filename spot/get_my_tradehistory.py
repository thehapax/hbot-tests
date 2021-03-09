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
          'startTime': 1611040430000} # works

# params = { 'orderID': 'a01416b4-96b7-429e-8ed4-33ee8bf06d0a', # this works
#         'startTime': 1606469000000 } 

params = {'clOrderID': 'buy-BTC-USDT-1606020895015706'} # this works - when testing, don't create a single client Order ID for multiple orders

#params = {'clOrderID': 'buy-BTC-USDT-1613877360'}

#params = {'clOrderID': '1741a782-588d-4bf3-8e5a-05f04c760a47',
#          'startTime': 1611040430000}

params = {'orderID': '2859d157-b6d3-4607-99ff-cfd19e85f6b2'}

# params = {'orderID': 'a01416b4-96b7-429e-8ed4-33ee8bf06d0a'}
#params = {'clOrderID': 'buy-BTC-USDT-1606020895015706'}

params = {'orderID': '54209b88-714c-4aa0-a4e1-c8aa7f91fc71'}

params = {'orderID': 'abad8f10-31ac-432d-a580-6b467e1ca0c2'}
params =  {'orderID': 'abad8f10-31ac-432d-a580-6b467e1ca0c2', 'startTime': 1615190714}

params = {'symbol': 'BTC-USDT'}


#params = {'orderID': 'b4c91383-c291-47c1-a3f6-d41531d87d0c'}

params = {"orderID":"db931935-541c-4201-97a6-99320a0af385"}

#params = {'orderID': '2859d157-b6d3-4607-99ff-cfd19e85f6b2'}

params = { 'orderID': 'a01416b4-96b7-429e-8ed4-33ee8bf06d0a'}  # this works
params = {'orderID': 'fb8f9422-7c90-4f3d-a5e3-369d2dcd00dc'}

#params = {'clOrderID': '1741a782-588d-4bf3-8e5a-05f04c760a47' }  #'startTime': 1615190714}
params = {'clOrderID' : 'buy-BTC-USDT-1613639646009553'} # 6 results for this 1 cl ID



fullpath = BTSE_Endpoint+path
print(f'REST API: {fullpath}')
print(f'Params: {params}')


r = requests.get(fullpath,
                params=params,
                headers=make_headers(path, ''))

result = r.json()
pp.pprint(result)

print(f'\n length of result {len(result)}')

