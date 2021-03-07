import ujson

BTSE_ENUM = {
1: "MARKET_UNAVAILABLE",
2: "ORDER_INSERTED",
4: "ORDER_FULLY_TRANSACTED",
5: "ORDER_PARTIALLY_TRANSACTED",
6: "ORDER_CANCELLED",
8: "INSUFFICIENT_BALANCE",
9: "TRIGGER_INSERTED",
10: "TRIGGER_ACTIVATED",
12: "ERROR_UPDATE_RISK_LIMIT",
28: "TRANSFER_UNSUCCESSFUL",
27: "TRANSFER_SUCCESSFUL",
41: "ERROR_INVALID_RISK_LIMIT",
64: "STATUS_LIQUIDATION",
101: "FUTURES_ORDER_PRICE_OUTSIDE_LIQUIDATION_PRICE",
1003: "ORDER_LIQUIDATION",
1004: "ORDER_ADL", 
404: "404 Error Cannot be Found"
}

def get_status_msg(code):
    msg = ''
    try:
        msg = BTSE_ENUM[code]
    except Exception as e:
        print(e)
    return msg 

# check if the string  is a json
def is_json(myjson):
    try:
        json_object = ujson.loads(myjson)
        if json_object:
            return True
    except ValueError:
        return False

def get_base(symbol):
    pairs = symbol.split('-')
    return pairs[0]

def get_quote(symbol):
    pairs = symbol.split('-')
    return pairs[1]

# get the min order size
'''
def get_min_ordersize(r):
      m = r.json()
      jm = m[0]
      #print(jm)
      minsize = jm['minOrderSize']
      print(f'\nmin order size: {minsize}\n')
      return minsize
'''

################## new methods to add to utils ################## 
import math
import requests
import locale
from decimal import Decimal

    
# round down to the nearest multiple of a
def round_down(x, a):
    return math.floor(x / a) * a

# round up - to use with minimum order size
def round_up(x, a):
    return math.ceil(x / a) * a
  
# round to the nearest multiple of a
def round_nearest(x, a):
    return round(x / a) * a

# adjust price for order based on btse size/price increment restrictions.
def adjust_increment(price, minpriceinc):
    try:
        price = Decimal(price)
        print(f'>> adjust_increment, input price: {price}, minpriceinc: {minpriceinc}\n')
        print(f'Type of minpriceinc {type(minpriceinc)}, price: {type(price)}\n')

        if 'e' in str(minpriceinc):
            p = Decimal(locale.format_string("%f", minpriceinc))
        else:
            p = Decimal(str(minpriceinc))
        
        min_price_decimals = len(str(p).split(".")[1])
        
        minpriceinc = Decimal(minpriceinc)
        print(f'Inside Adjust_increment: min price inc: {minpriceinc},' +
              f' number of decimals allowed: {min_price_decimals}\n\n')
        print(f' Type of min_price_decimals: {type(min_price_decimals)}')
        
        deci = price - math.floor(price)
        if deci == 0:
            adjusted_price = price
            print(f'\n Deci - adjusted price is price: {price}')
            return adjusted_price 
        
        remainder = Decimal(deci) % minpriceinc
        # type of minprice in is float by default?
        print(f'Type of minpriceinc {type(minpriceinc)}, deci: {type(deci)}\n')
        print(f'Type of remainder {type(remainder)}\n')

        if remainder == 0.0: # we are at no remainder so obeys step. 
            adjusted_price = price
            print(f'remainder - adjusted price is price: {price}')
        else: 
            near_price = round_nearest(price, minpriceinc)
            adjusted_price = round(near_price, min_price_decimals)
            print(f'round_nearest price: {near_price}, adj_price: {adjusted_price}')

        return adjusted_price
    except Exception as e:
        print(f'Exception thrown in adjust_increment: {e}')
        return e

# Calculate size for order within btse exchange bounds
def bounded_size(size, minsize, maxsize, minsizeinc):
    try:
        adjusted_size = size
        min_sizeinc = minsizeinc
        min_size = minsize

        print(f">> \nBounded_size - input size (float): {adjusted_size}," +
              f"Minsize {minsize}," + 
              f"Maxsize {maxsize}, minsizeinc {minsizeinc}\n")
        
        if 'e' in str(minsizeinc):
            min_sizeinc = Decimal(locale.format_string("%f",minsizeinc))
        if 'e' in str(minsize):
            min_size = Decimal(locale.format_string("%f", minsize))

        minsizeinc_decimals = len(str(min_sizeinc).split(".")[1])
        print(f'\n minsize_inc decimals: {minsizeinc_decimals}')
        print(f'\n min_sizeinc: {min_sizeinc}, min_size: {min_size}\n')

        if size < maxsize and size > min_size:
            print("adjusted size within bounds, ok")
            adjusted_size = size
        elif size <= min_size:
            print("make minsize adjusted size")
            adjusted_size = min_size
        elif size >= maxsize:
            print("make adjusted_size maxsize")
            adjusted_size = maxsize
        print(f'\n>> post switch adjusted_size: {adjusted_size}')
        # min size decimals 
        
        #bounded_size = round_up(float(adjusted_size), float(min_sizeinc))
        bounded_size = round_up(Decimal(adjusted_size), Decimal(min_sizeinc))
        print(f'>> Bounded Adjusted Size: {bounded_size}, minsize: {min_sizeinc}')
        bounded_size = round(bounded_size, minsizeinc_decimals)
        print(f'\n bounded size rounded off : {bounded_size}')
        
        return bounded_size
    except Exception as e:
        print(f'Exception in bounded_size: {e}')
        return e

# for testing get one market size and price based on avg market price
# mkt = get_market(params)

headers = {
  'Accept': 'application/json;charset=UTF-8'
}
BTSE_Endpoint = 'https://testapi.btse.io/spot'


def get_one_market(params, size, price):
    try:
        mkt = requests.get(BTSE_Endpoint+'/api/v3.2/market_summary', 
                           params=params, 
                           headers=headers)
        mkt_info = mkt.json()
        info = mkt_info[0]
        minsize = info['minOrderSize']
        maxsize = info['maxOrderSize']
        minsizeinc = info['minSizeIncrement']
        minpriceinc = info['minPriceIncrement']
        minvalidprice =  info['minValidPrice']

        print(f'Min Price Increment: {minpriceinc}, min valid price: {minvalidprice}')
        print(f'Type of minpriceinc {type(minpriceinc)}, price: {type(price)}\n')

        adjusted_price = adjust_increment(price, minpriceinc)
        final_size = bounded_size(size, minsize, maxsize, minsizeinc)
        return adjusted_price, final_size
    
    except Exception as e:
        return e

##### new methods to add to utils ######### 


# 'symbol': 'BTC-USD', 
if __name__ == "__main__":
    
    response = {"status":2,"symbol":"BTC-USDT",
                "orderType":76,"price":7050.0,
                "side":"BUY","size":0.002,
                "orderID":"63763850-adca-43b6-a642-7912c7ddebaf",
                "timestamp":1603931889411,"triggerPrice":0.0,
                "stopPrice":'null',"trigger":'false',"message":""}
    
    code = response['status']
    print(type(code))
    print(code)
    
    msg = get_status_msg(code)
    print(f'Status message from code: {msg}')
    