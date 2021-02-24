WS_SOCKET:

 {"topic":"notificationApiV1",
    "data":{"averageFillPrice":57540.0,
            "clOrderID":"sell-BTC-USDT-1613879426212116",
            "fillSize":0.006,
            "maker":True,
            "orderID":"b0a9beaf-a0d2-4236-9536-8ab55d741011",
            "orderMode":"MODE_SELL",
            "orderType":"TYPE_LIMIT",
            "pegPriceDeviation":1.0,
            "postOnly":False,
            "price":57540.0,
            "remainingSize":0.094,
            "size":0.001,
            "status":"ORDER_PARTIALLY_TRANSACTED",
            "stealth":1.0,
            "symbol":"BTC-USDT",
            "time_in_force":"GTC",
            "timestamp":1613987076539,
            "triggerPrice":57540.0,"type":""}}


WS_SOCKET: 
    
    {"topic":"notificationApiV1",
     "data":{
         "averageFillPrice":57540.0,
         "clOrderID":"buy-BTC-USDT-1613987076008351",
         "fillSize":0.001,
         "maker":false,
         "orderID":"a149becf-8575-42bc-9257-bdd061c9671c",
         "orderMode":"MODE_BUY",
         "orderType":"TYPE_LIMIT",
         "pegPriceDeviation":1.0,
         "postOnly":false,
         "price":57540.0,
         "remainingSize":0.0,
         "size":0.001,
         "status":"ORDER_FULLY_TRANSACTED",
         "stealth":1.0,
         "symbol":"BTC-USDT","time_in_force":"GTC",
         "timestamp":1613987076539,
         "triggerPrice":60417.0,
         "type":""}}
    
    
    Trade history
    
    REST API: https://testapi.btse.io/spot/api/v3.2/user/trade_history
Params: {'orderID': '54209b88-714c-4aa0-a4e1-c8aa7f91fc71'}
make_headers - MESSAGE: /api/v3.2/user/trade_history1614032491917

[   {   'base': 'BTC',
        'clOrderID': None,
        'feeAmount': 0.479504033,
        'feeCurrency': 'USDT',
        'filledPrice': 47950.403348186,
        'filledSize': 0.01,
        'orderId': '54209b88-714c-4aa0-a4e1-c8aa7f91fc71',
        'orderType': 77,
        'price': 47950.403348186,
        'quote': 'USDT',
        'realizedPnl': 0.0,
        'serialId': 130720344,
        'side': 'SELL',
        'size': 0.01,
        'symbol': 'BTC-USDT',
        'timestamp': 1613878716000,
        'total': 0.0,
        'tradeId': '692c77c5-ef21-41fc-8381-a37ae903678e',
        'triggerPrice': 0.0,
        'triggerType': 0,
        'username': 'hapax10test',
        'wallet': 'SPOT@'}]


>>>>> process_trade_msg - track_order: 
    
    [InFlightOrder(client_order_id='buy-BTC-USDT-1613987076008351', 
                   exchange_order_id='a149becf-8575-42bc-9257-bdd061c9671c',
                   trading_pair='BTC-USDT', 
                   order_type=OrderType.LIMIT, 
                   trade_type=TradeType.BUY, 
                   price=60417.00, 
                   amount=0.001, 
                   executed_amount_base=0, 
                   executed_amount_quote=0, 
                   fee_asset='None', 
                   fee_paid=0, 
                   last_state='OPEN')]
    
    
    async def _process_trade_message(self, trade_msg: Dict[str, Any]):
        """
        Updates in-flight order and trigger order filled event for trade message received. Triggers order completed
        event if the total executed amount equals to the specified order amount.
        """ 
            example trade history from REST API:
          {   'base': 'BTC',
        'clOrderID': None,
        'feeAmount': 2e-06,
        'feeCurrency': 'BTC',
        'filledPrice': 10758.0,
        'filledSize': 0.002,
        'orderID': 'b3a65f8e-e838-4c13-adf4-62fef98504a1',
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



    # for btse, filled completed orders with fees (tradehistory)
    # def _process_order_message(self, order_msg: Dict[str, Any]):
        """
        Updates in-flight order and triggers cancellation or failure event if needed.
        :param order_msg: The order response from web socket API
        (REST API not same format, only open orders)
        """
        
        example from notificationsAPI websocket:
        {   'averageFillPrice': 0.0,
                'clOrderID': 'MYOWNORDERID',
                'fillSize': 0.0,
                'orderID': '01d9a550-4acd-4f12-990f-ef496f325a7b',
                'orderMode': 'MODE_BUY',
                'orderType': 'TYPE_LIMIT',
                'pegPriceDeviation': 1.0,
                'price': 7010.0,
                'size': 0.002,
                'status': 'ORDER_INSERTED',
                'stealth': 1.0,
                'symbol': 'BTC-USD',
                'timestamp': 1602229225728,
                'triggerPrice': 7010.0,
                'type': ''},
                'topic': 'notificationApiV1'}



==================


    #### DEFINITELY OPTIONAL ######
    # rest alternative if needed - check pls. add to update_order_status
    # _process_order -  open orders or none for rest api
    async def _get_open_order_status(self):
        """
        Calls REST API to get open order status update for each in-flight order.
        """
        print(f'\nINSIDE _get_open_order_status\n\n')
        tasks = []
        # need to specify which symbol - post for all? vs get? 
        pairs = self.trading_pairs
        # todo 2/18/21 - check this param works
        
        # params = {}
        for pair in pairs:
            print(f'\n _get_open_order_status Trading pair: {pair}')
            params = {'symbol': pair}         
            tasks.append(self._api_request(method="post", 
                                        path="user/open_orders", 
                                        params=params, 
                                        is_auth_required=True))
        
        self.logger().debug(f"Polling for open order status updates of {len(tasks)} orders.")
        update_results = await safe_gather(*tasks, return_exceptions=True)
        for update_result in update_results:
            if isinstance(update_result, Exception):
                raise update_result
            if not update_result:
                self.logger().info(f"_get_open_order_status result not in resp: {update_result}")
                continue
            for trade_msg in update_result:
                print("trade_msg from get_open_order_status")
                await self._process_order_message(trade_msg)
