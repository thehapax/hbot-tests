from btseauth_spot import BTSE_Endpoint, make_headers
from decimal import Decimal

BTSE_Endpoint = 'https://testapi.btse.io/spot'

# open orders
open_order_params = {'symbol': 'ETH-USDT'}
open_path = '/api/v3.2/user/open_orders'
url = BTSE_Endpoint+open_path

# limit_orders
limit_path = '/api/v3.2/order'
limit_url = BTSE_Endpoint+limit_path

# del order
del_path = '/api/v3.2/order'
delete_url = BTSE_Endpoint+del_path

price = 335.1500000000000253769227854
price = Decimal('%.7g' % price)

limit_order_form = {"symbol": "ETH-USDT", "side": "BUY", "type": "LIMIT",
                     "price": f"{price:f}", 
                     "size": "0.09800000000000000204003480775", 
                     "triggerPrice": 0, "time_in_force": "GTC", 
                     "txType": "LIMIT", "clOrderID": "buy-ETH-USDT-1604374232705551"}

cancel_params = {'orderID': 'b83baf19-7ebe-4997-bfc1-648b06985ad4',
                    'symbol': 'ETH-USDT'}

open_order_params = {'symbol': 'ETH-USDT'}


