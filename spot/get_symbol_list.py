
from btseauth_spot import BTSE_Endpoint
import requests
import pprint 
import json
from decimal import Decimal
import math

BTSE_Endpoint = 'https://testapi.btse.io/spot'

pp = pprint.PrettyPrinter(indent=4)

r = requests.get(BTSE_Endpoint+'/api/v3.2/market_summary')
#res = r.json()
res = json.loads(r.text)

print("----")
#pp.pprint(res)
print("----")

for rule in res:
    trading_pair = rule['symbol']
    price_step = rule['minPriceIncrement']
    quantity_step = rule['minSizeIncrement']
    entry = {}
    entry['symbol'] = trading_pair
    entry['price_step'] = price_step
    entry['quantity_step'] = quantity_step
    print(f'\n{entry}')
    
    print("Price Step: ")
    print(price_step)
    price_decimals = Decimal(str(price_step))
    price_step2 = Decimal("1") / Decimal(str(math.pow(10, price_decimals)))
    print(price_step2)

'''
conver float to decimal? is it needed?

    print("price step: ")
    print(type(price_step))
    print("quantity step of base asset: ")
    print(type(quantity_step)) # type is float
    
price step: 
<class 'float'>
quantity step of base asset: 
<class 'float'>
'''