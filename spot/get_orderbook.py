# From BTSE Public Endpoints -
# https://www.btse.com/apiexplorer/spot/?python#btse-spot-api-public-endpoints
# get market summary, ohlcv
# get orderbook L1 and L2
# get price, trades, epoch time
import requests
import pprint
import time

# requires symbol
main_url = 'https://api.btse.com/spot'
market_summary = 'https://api.btse.com/spot/api/v3.2/market_summary'
ohlcv = 'https://api.btse.com/spot/api/v3.2/ohlcv'
L1 = 'https://api.btse.com/spot/api/v3.2/orderbook'
L2 = 'https://api.btse.com/spot/api/v3.2/orderbook/L2'
price = 'https://api.btse.com/spot/api/v3.2/price'
trades = 'https://api.btse.com/spot/api/v3.2/trades'

# does not require symbol
epoch_time = 'https://api.btse.com/spot/api/v3.2/time'
pp = pprint.PrettyPrinter(indent=4)
symbol = 'BTC-USDT'

headers = {
  'Accept': 'application/json;charset=UTF-8'
}

def get_main():
    r = requests.get(main_url,
                     params={}, 
                     headers= headers)
    print(type(r))
    print(r.text)
    return r.json()

def get_market(symbol):
    print("\n======= GET Market Summary ======")
    r = requests.get(market_summary, 
                    params={'symbol': symbol}, 
                    headers = headers)
    pp.pprint(r.json())
    return r.json()


def get_epochtime():
    print("\n======= GET Epoch Time ======")
    r = requests.get(epoch_time, 
                    headers = headers)
    pp.pprint(r.json())
    return r.json()


def get_l1(symbol):
    print("\n======= GET L1 Orderbook  ======")
    r = requests.get(L1, 
                    params={'symbol': symbol}, 
                    headers = headers)
    pp.pprint(r.json())
    return r.json()


def get_l2(symbol):
    print("\n======= GET L2 Orderbook ======")
    r = requests.get(L2, 
                    params={'symbol': 'BTC-USD'}, 
                    headers = headers)
    pp.pprint(r.json())
    return r.json()


def get_price(symbol):
    print("\n======= GET PRICE ======")
    r = requests.get(price, 
                    params={'symbol': symbol}, 
                    headers = headers)
    pp.pprint(r.json())
    return r.json()


def get_trades(symbol):
    print("\n======= GET TRADES ======")
    r = requests.get(trades, 
                    params={'symbol': symbol}, 
                    headers = headers)
    pp.pprint(r.json())
    return r.json()


def get_ohlcv(symbol):
    print("\n======= GET OHLCV ======")
    r = requests.get(trades, 
                    params={'symbol': symbol}, 
                    headers = headers)
    pp.pprint(r.json())
    return r.json()


def get_orderbook_data(result): # use L2 orderbook with timestamp
    result['bids'] = result.pop('buyQuote')
    result['asks'] = result.pop('sellQuote')
    bids = result['bids']
    asks = result['asks']
    ts = result['timestamp']
    symbol = result['symbol']
    mbids = result.items()
    print("extract==")
    print(mbids)
    

if __name__ == "__main__":
    #r = get_main()
    
    result = get_market(symbol)
    '''
    ohlcv = get_ohlcv(symbol) # this is broken on the BTSE Api side
    '''
    
#    result = get_epochtime()
 
    result = get_l1(symbol)
#    result = get_price(symbol)
#    result = get_trades(symbol)
#    get_orderbook_data(result)
'''
    result = get_l2(symbol)
    
    print("============")
    print(time.time())
    bids = []
    asks = []
    for i in result['buyQuote']:
        bids.append(list(i.values()))
    for i in result['sellQuote']:
        asks.append(list(i.values()))
    print(time.time())

    ob = {'timestamp' : result['timestamp'], 'symbol': result['symbol']} 
    ob['bids'] = bids
    ob['asks'] = asks   
    pp.pprint(ob)

'''


'''
result from get L2 order book

{   'buyQuote': [   {'price': '10232.0', 'size': '0.308'},
                    {'price': '10230.5', 'size': '0.199'},
                    {'price': '10228.5', 'size': '0.930'},
                    {'price': '2565.5', 'size': '0.100'}],
    'sellQuote': [   {'price': '29850.0', 'size': '1.892'},
                     {'price': '10234.0', 'size': '0.110'},
                     {'price': '10233.5', 'size': '0.302'}],
    'symbol': 'BTC-USD',
    'timestamp': 1600897059891}

'''