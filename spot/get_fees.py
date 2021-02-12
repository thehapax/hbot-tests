import requests
import json
from btseauth_spot import BTSE_Endpoint, make_headers
import pprint

pp = pprint.PrettyPrinter(indent=4)

path = '/api/v3.2/user/fees'
params={'symbol': 'BTC-USD'}
# params={}  # returns error: {'code': -1, 'data': None, 'msg': None, 'success': False, 'time': 1612487445206}

r = requests.get(BTSE_Endpoint+path,
                params=params,
                headers=make_headers(path, ''))

pp.pprint(r.json())

'''
example selected response: for symbol 'BTC-USD'
[{'symbol': 'BTC-USD', 'makerFee': 0.0005, 'takerFee': 0.001}]
'''

'''
example full response: 

[   {'makerFee': 0.0005, 'symbol': 'LEO-USD', 'takerFee': 0.001},
    {'makerFee': 0.0005, 'symbol': 'TRX-USD', 'takerFee': 0.001},
    {'makerFee': 0.0005, 'symbol': 'STAKE-USD', 'takerFee': 0.001},
    {'makerFee': 0.0005, 'symbol': 'BCB-USD', 'takerFee': 0.001},
    {'makerFee': 0.0005, 'symbol': 'BTSE-USD', 'takerFee': 0.001},
    {'makerFee': 0.0005, 'symbol': 'XRP-USD', 'takerFee': 0.001},
    {'makerFee': 0.0005, 'symbol': 'TR_USDT-USD', 'takerFee': 0.001},
    {'makerFee': 0.0005, 'symbol': 'LTC-USD', 'takerFee': 0.001},
    {'makerFee': 0.0005, 'symbol': 'ETH-USD', 'takerFee': 0.001},
    {'makerFee': 0.0005, 'symbol': 'USDT-USD', 'takerFee': 0.001},
    {'makerFee': 0.0005, 'symbol': 'BRZ-USD', 'takerFee': 0.001},
    {'makerFee': 0.0005, 'symbol': 'BTC-USD', 'takerFee': 0.001},
    {'makerFee': 0.0005, 'symbol': 'XMR-USD', 'takerFee': 0.001},
    {'makerFee': 0.0005, 'symbol': 'XAUT-USD', 'takerFee': 0.001}]
'''
