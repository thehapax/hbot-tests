# get spot market summary, e.g. https://api.btse.com/spot/api/v3.2/market_summary?symbol=BTC-USD
'''
# sample from 11.28.2020

[{'symbol': 'BTC-USDT', 'last': 17873.0, 'lowestAsk': 17867.0, 'highestBid': 17685.0, 
'percentageChange': 6.000476701, 'volume': 177198.857630865, 'high24Hr': 17873.003114639, 
'low24Hr': 16861.247864965, 'base': 'BTC', 'quote': 'USDT', 'active': True, 'size': 10.249, 
'minValidPrice': 0.5, 'minPriceIncrement': 0.5, 'minOrderSize': 0.001, 'maxOrderSize': 2000.0,
'minSizeIncrement': 0.001, 'openInterest': 0.0, 'openInterestUSD': 0.0, 'contractStart': 0, 
'contractEnd': 0, 'timeBasedContract': False, 'openTime': 0, 'closeTime': 0, 'startMatching': 0,
'inactiveTime': 0, 'fundingRate': 0.0, 'contractSize': 0.0, 'maxPosition': 0, 'minRiskLimit': 0, 
'maxRiskLimit': 0, 'availableSettlement': None, 'futures': False}
'''

from btseauth_spot import BTSE_Endpoint
import requests
import pprint 
import math

pp = pprint.PrettyPrinter(indent=4)
headers = {
  'Accept': 'application/json;charset=UTF-8'
}
BTSE_Endpoint = 'https://testapi.btse.io/spot'


# get the min order size
def get_min_ordersize(r):
      m = r.json()
      jm = m[0]
      #print(jm)
      minsize = jm['minOrderSize']
      print(f'\nmin order size: {minsize}\n')
      return minsize
    
# round down to the nearest multiple of a
def round_down(x, a):
    return math.floor(x / a) * a

# round up - to use with minimum order size
def round_up(x,a):
    return math.ceil(x / a) * a
  
# round to the nearest multiple of a
def round_nearest(x, a):
    return round(x / a) * a

# adjust price for order based on btse size/price increment restrictions.
def adjust_increment(info, price, size):
    minsizeinc = info['minSizeIncrement']
    minpriceinc = info['minPriceIncrement']
    print(f'\nMin Price Increment: {minpriceinc}')
    
    adjusted_price = round_nearest(price, minpriceinc)
    print(f'>> Adjusted Price : {adjusted_price}')
 
    print(f'\nMin Size Increment: {minsizeinc}')   
    adjusted_size = round_up(size, minsizeinc)
    print(f'>> Adjusted Size: {adjusted_size}')
    return adjusted_price, adjusted_size
    

# Calculate size for order within btse exchange bounds
def bounded_size(adjusted_size, minsize, maxsize):
  print(f"\nExchange Minsize {minsize}, Maxsize {maxsize}")
  if adjusted_size < maxsize and adjusted_size > minsize:
        print("adjusted size within bounds, ok")
        return adjusted_size
  elif adjusted_size <= minsize:
        print("make minsize adjusted size")
        return minsize
  elif adjusted_size >= maxsize:
        print("make adjusted_size maxsize")
        return maxsize


def get_market(params):
  r = requests.get(BTSE_Endpoint+'/api/v3.2/market_summary', params=params, headers = headers)
  return r


def get_one_market(params, size):
  mkt = get_market(params)
  mkt_info = mkt.json()
  
  info = mkt_info[0]
  pp.pprint(info)

  lAsk = info['lowestAsk']
  hBid = info['highestBid'] 
  symbol = info['symbol']

  # Example: take the average of low Ask and high Bid for your new limit order
  price = (lAsk + hBid)/2
  
  adjusted_price, adjusted_size = adjust_increment(info, price, size)
  
  minsize = info['minOrderSize']
  maxsize = info['maxOrderSize']
  final_size = bounded_size(adjusted_size, minsize, maxsize)

  print(f'\n >>> Symbol: {symbol},\n Order Size desired: {size}')
  print(f'\n lowest Ask {lAsk}, highest Bid: {hBid}')  
  print(f'\nadjusted price {adjusted_price}, adjusted size {final_size}, pre-adjusted size {adjusted_size}')
  print("==============================")
  return adjusted_price, final_size

  
def get_all_markets(size):
  params = {}  # get all market info
  mkt = get_market(params)
  mkt_info = mkt.json()
  # pp.pprint(mkt_info)
  num_symbols = len(mkt_info)
  print(f'total pairs: {num_symbols}')

  index = 0

  for info in mkt_info:
    symbol = info['symbol']
    lAsk = info['lowestAsk']
    hBid = info['highestBid']
    price = (lAsk + hBid)/2

    print(f'\n >>> Symbol: {symbol},\n low24 price: {price},\n size: {size}')
    adjusted_price, adjusted_size = adjust_increment(mkt_info[index], price, size)
    
    minsize = info['minOrderSize']
    maxsize = info['maxOrderSize']
    a_size = bounded_size(adjusted_size, minsize, maxsize)
    
    print(f'\nadjusted price {adjusted_price}, adjusted size {a_size}, pre-adjusted size {adjusted_size}')
    print("==============================")



if __name__ == '__main__':
  #params = {'symbol': 'ETH-USDT'}
  params = {'symbol': 'BTC-USDT'}
  print(f'params: {params}\n')
  size = 0.05  # this is the size of the order to be placed on exchange.
  get_one_market(params, size)
  get_all_markets(size)



#################

# min order size
# min size increment at 0.001 - 3 digits
# minPriceIncrement - important that price increment in these intervals of 0.5 only
# 'minOrderSize': 0.001,
# 'maxOrderSize': 2000.0,
# 'last': 36639.5,
# 'size': 4036.991, - size refers the 24 volume
# 'base': 'BTC'
# 'quote': 'USDT'
#  minsizeinc = 0.05
#  minpriceinc = 1e-08

'''
from market exchange crypto.com example
result[trading_pair] = TradingRule(trading_pair,
                                  min_price_increment=price_step,
                                  min_base_amount_increment=quantity_step)
'''

'''
example: 
[   {   'active': True,
        'availableSettlement': None,
        'base': 'BTC',  ### ---- base
        'closeTime': 0,
        'contractEnd': 0,
        'contractSize': 0.0,
        'contractStart': 0,
        'fundingRate': 0.0,
        'futures': False,
        'high24Hr': 10758.0,
        'highestBid': 10757.5,
        'inactiveTime': 0,
        'last': 10758.0,
        'low24Hr': 10741.5,
        'lowestAsk': 10758.0,
        'maxOrderSize': 2000.0,
        'maxPosition': 0,
        'maxRiskLimit': 0,
        
        'minOrderSize': 0.001, # ------
        'minPriceIncrement': 0.5,  ##  xxxxxxxx
        'minRiskLimit': 0,
        'minSizeIncrement': 0.001, ## xxxxxx
        
        'minValidPrice': 0.5,
        'openInterest': 0.0,
        'openInterestUSD': 0.0,
        'openTime': 0,
        'percentageChange': 0.00464792,
        'quote': 'USD', # ----- quote 
        'size': 0.766,
        'startMatching': 0,
        'symbol': 'BTC-USD', # --------
        'timeBasedContract': False,
        'volume': 8240.5455}]
'''

'''
crypto.com get markets
 Response Example:
        {
            "id": 11,
            "method": "public/get-instruments",
            "code": 0,
            "result": {
                "instruments": [
                      {
                        "instrument_name": "ETH_CRO",
                        "quote_currency": "CRO",
                        "base_currency": "ETH",
                        "price_decimals": 2,
                        "quantity_decimals": 2
                      },
                      {
                        "instrument_name": "CRO_BTC",
                        "quote_currency": "BTC",
                        "base_currency": "CRO",
                        "price_decimals": 8,
                        "quantity_decimals": 2
                      }
                    ]
              }
        }
'''
