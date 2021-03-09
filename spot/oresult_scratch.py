

order_result = [{'status': 2, 'symbol': 'BTC-USDT', 'orderType': 76, 
                 'price': 47050.0, 'side': 'BUY', 'size': 0.002, 
                 'orderID': '67a8a22e-14a9-413f-a138-09abe3a3e4bc', 'timestamp': 1613640811304, 
                 'triggerPrice': 0.0, 'stopPrice': None, 'trigger': False, 'message': '', 
                 'averageFillPrice': 0.0, 'fillSize': 0.0, 'clOrderID': 'buy-BTC-USDT-1613640810753537', 
                 'stealth': 1.0, 'deviation': 1.0, 'postOnly': False, 'time_in_force': 'GTC'}]


order_id = order_result[0]['orderID']
print(f'order_id: {order_id}')


amt = 0.000123456
bid_price =  44786.489862732783706125