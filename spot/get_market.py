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
from utils import adjust_increment, bounded_size
import requests
import pprint
import sys

pp = pprint.PrettyPrinter(indent=4)
headers = {
  'Accept': 'application/json;charset=UTF-8'
}
BTSE_Endpoint = 'https://testapi.btse.io/spot'

def get_market(params):
  url = BTSE_Endpoint+'/api/v3.2/market_summary'
  #print(f'get_market params: {params},\n headers: {headers}, \n url: {url}')
  r = requests.get(url, params=params, headers = headers)
  return r

#############################################

# for testing get one market size and price based on avg market price
def get_a_market(params, size):
  mkt = get_market(params)
  mkt_info = mkt.json()
  info = mkt_info[0]
  minsize = info['minOrderSize']
  maxsize = info['maxOrderSize']
  minsizeinc = info['minSizeIncrement']
  minpriceinc = info['minPriceIncrement']
  minvalidprice =  info['minValidPrice']

  lAsk = info['lowestAsk']
  hBid = info['highestBid'] 
  ### TODO -- 'minValidPrice': 0.5 ??
  
  last = info['last']
  print(f'\n\nLast Price on Market: {last}')
  # symbol = info['symbol']
  
  # Example: take the average of low Ask and high Bid for your new limit order
  # if you want to set a price otherwise, skip this or use your own pricing metric
  
  price = (lAsk + hBid)/2
  
  price_quantized = adjust_increment(price, minpriceinc)
  
  if price_quantized < minvalidprice:
      price_quantized = minvalidprice
  print(f'>> get_order_price_quantum - Quantized Price : {price_quantized}')

  final_size = bounded_size(size, minsize, maxsize, minsizeinc)

  pp.pprint(info)
  #print(f'\n Symbol: {symbol} lowest Ask {lAsk}, highest Bid: {hBid}')
  #print(f'pre-adjusted size {adjusted_size}')

  return price_quantized, final_size

  
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
    print(f'Symbol: {symbol}')
    minvalidprice =  info['minValidPrice']
    minpriceinc = info['minPriceIncrement']
    
    #if 'ATOM' in symbol:
    try:
      print(f'\n >>> Symbol: {symbol},\n low24 price: {price},\n size: {size}')
      adjusted_price = adjust_increment(price, minpriceinc, minvalidprice)
      
      minsize = info['minOrderSize']
      maxsize = info['maxOrderSize']
      a_size = bounded_size(size, minsize, maxsize, info['minSizeIncrement'])
      
      last = info['last']
      print(f'\n\nLast Price on Market: {last}')

      print(f'\nadjusted price {adjusted_price}, adjusted size {a_size}, pre-adjusted size {size}')
      print("==============================")
    except Exception as e:
      print(f'Error on Conversion: {e}')
    


if __name__ == '__main__':

  size = 0.05  # this is the size of the order we would like to place on exchange.
  symbol = 'ETH-USDT'
  if len(sys.argv[1:]) != 0:
        symbol = sys.argv[1]

  params = {'symbol': f'{symbol}'}  
  adjusted_price, final_size =  get_a_market(params, size)
  
  print(f'\n >>> Symbol: {symbol},\n ')
  print(f'params: {params}, Order Size Desired: {size} \n')
  print(f'\nadjusted price {adjusted_price}, adjusted size {final_size}')
  print("==============================")
  
  # get all market information and adjust price and size to within btse bounds
  # get_all_markets(size)



####################################################################
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
####################################################################

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
