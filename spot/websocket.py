import asyncio
import ujson
import hmac
import hashlib
import time
import websockets
import pprint
import ujson

from btseauth_spot import gen_auth, keypair, BTSE_WSEndpoint
from PeriodicChecker import PeriodicChecker

# works on testnet and production

# ping checker for keep alive with websocket, aka heartbeat
ping_checker = PeriodicChecker(period_ms = 8 * 1000)
pp = pprint.PrettyPrinter(indent=4)


def subscription_payload():
    # notificationApi is private data
    payload = {'op': 'subscribe', 'args': ['notificationApiV1']}

    print("sending subscription V1 payload")
    return payload

def orderbook_payload():
    # Order book subscription, 5 levels, public data
    payload = {
        "op":"subscribe",
        "args":["orderBookL2Api:BTC-USDT_5"] # up to 150 entries
    }
    print("sending order book btc-usdt-5 payload")
    return payload

def tradehistory_payload():
    # combined tradehistory and orderbook api
    # tradehistory is public data
    payload = {
        "op":"subscribe",
        "args":["tradeHistoryApi:BTC-USDT"]
    }
    return payload

def process_orderbook_data(ob):
    bids = ob['data']['buyQuote']
    asks = ob['data']['sellQuote']
    print("===== Bids =====")
    print(bids)
    print("==== Asks =====")
    print(asks)

def get_event_responses(response):        
    '''
    if channel list doesn't match payload list 
    When subscribing or unsubscribing to websocket topics, an acknowledgement 
    will return to indicate which topics are successfully subscribed / unsubscribed. 
    Unsuccessful topics are not returned in the response
    Examples: 
    {"event":"login","success":true}
    {"event":"subscribe","channel":["tradeHistoryApi:BTC-USDT","notificationApiV1:"]}
    {"code":10002,"success":false,"time":1613279439623}
    '''
    
    lookup = {'login' : 'success', 'subscribe': 'channel'}
    ## Need method to check subscriptions against payload args.  
    
    print(f'response {response}')
    res = ujson.loads(response)
    
    status = ''
    if 'login' in response: 
        status = res['success']
    elif 'subscribe' in response:
        status = res['channel']
    elif 'code' in response: # error code
        status = res['code']
    
    print(f'status: {status}, type: {type(status)}')
    return status            
    
async def connect_forever():
    path = '/spotWS'
    url = BTSE_WSEndpoint + path
    
    async with websockets.connect(url) as websocket:
        # Authentication
        auth = gen_auth(keypair['API-KEY'], keypair['API-PASSPHRASE'])
        print("***** GEN AUTH: *****" + str(auth))
        auth_payload = ujson.dumps(auth)
        await websocket.send(auth_payload)
        
        # Subscription - order notifications
        user_payload = subscription_payload()
        ob_payload = orderbook_payload()
        trade_payload = tradehistory_payload()
        await websocket.send(ujson.dumps(user_payload))
        # await websocket.send(ujson.dumps(ob_payload))
        await websocket.send(ujson.dumps(trade_payload))

        MESSAGE_TIMEOUT = 30.0

        while True:
            try:
                response: Dict[Any] = await asyncio.wait_for(websocket.recv(), timeout=MESSAGE_TIMEOUT)
                print("\n======= WEBSOCKET DATA RECEIVED: ======= \n")
                print(response)
                code = get_event_responses(response)
                #print(f'Event status: {str(code)}')
                
                if 'topic' in response:
                    print(type(response))
                    r = ujson.loads(str(response))
                    topic = r['topic']
                    print(f'topic: {topic}')
                    
                                    
                '''
                if "topic" in response:
                    r = ujson.loads(str(response))
                    if "orderBookApi" in r['topic']:
                        process_orderbook_data(r)
                        pp.pprint(r)
                    elif "tradeHistoryApi" in r['topic']:
                        # pp.pprint(r)
                        data = r['data']
                        # pp.pprint(data)
                        for trade in r["data"]:
                            trade: Dict[Any] = trade
                            print(trade)
                    elif "notificationsApi" in r['topic']:
                        print("notifications")
                        data = r['data']
                        pp.pprint('data')
                else:
                    print("No topic in response")
                    code = get_auth_responses(response)
                    print(type(code))
                    print(code)
                '''
            except Exception as e:
                print(e)

            if ping_checker.check():
                payload = {"op": "ping"}
                print("==== Keep Alive HEART BEAT === sending a ping: " + str(payload))
                await websocket.send(ujson.dumps(payload))


asyncio.get_event_loop().run_until_complete(connect_forever())


'''
Sample process_orderbook_data result:
===== Bids =====
[{'price': '10247.0', 'size': '0.112'}, {'price': '10246.5', 'size': '0.471'}, {'price': '10246.0', 'size': '0.237'}, {'price': '10245.0', 'size': '0.319'}, {'price': '10243.5', 'size': '0.960'}, {'price': '10243.0', 'size': '1.119'}, {'price': '10242.5', 'size': '1.288'}, {'price': '10242.0', 'size': '2.521'}, {'price': '10241.5', 'size': '3.273'}, {'price': '10240.5', 'size': '0.466'}]
==== Asks =====
[{'price': '10262.5', 'size': '0.286'}, {'price': '10262.0', 'size': '0.438'}, {'price': '10258.0', 'size': '0.610'}, {'price': '10257.5', 'size': '0.198'}, {'price': '10257.0', 'size': '0.281'}, {'price': '10256.5', 'size': '0.138'}, {'price': '10256.0', 'size': '0.161'}, {'price': '10255.5', 'size': '0.304'}, {'price': '10254.5', 'size': '0.092'}, {'price': '10254.0', 'size': '0.332'}]
'''

'''
Sample trade history result:

{   'data': [   {   'price': 10758.0,
                    'side': 'BUY',
                    'size': 0.092,
                    'symbol': 'BTC-USD',
                    'timestamp': 1601873979246,
                    'tradeId': 110985476},
                {   'price': 10500.0,
                    'side': 'BUY',
                    'size': 5.0,
                    'symbol': 'BTC-USD',
                    'timestamp': 1601213574958,
                    'tradeId': 110722582},
                {   'price': 10500.0,
                    'side': 'BUY',
                    'size': 25.0,
                    'symbol': 'BTC-USD',
                    'timestamp': 1601213564931,
                    'tradeId': 110722580}],
    'topic': 'tradeHistoryApi:BTC-USD'}
    
    '''
    

# Raw order book  data:
'''
    {'data': { 'buyQuote': [    {'price': '10600.0', 'size': '200.002'},
                                {'price': '10500.0', 'size': '620.000'},
                                {'price': '7000.0', 'size': '0.002'},
                                {'price': '1000.0', 'size': '1.000'},
                                {'price': '100.0', 'size': '0.003'},
                                {'price': '0.0', 'size': '34.016'}],
                'currency': 'USD',
                'sellQuote': [   {'price': '113700.0', 'size': '0.001'},
                                    {'price': '12000.0', 'size': '6.740'},
                                    {'price': '11800.0', 'size': '5095.000'},
                                    {'price': '11600.0', 'size': '185.000'},
                                    {'price': '11500.0', 'size': '525.000'},
                                    {'price': '11400.0', 'size': '75.000'},
                                    {'price': '10900.0', 'size': '38859.849'}],
                'symbol': 'BTC-USD',
                'timestamp': 1602890445777},
        'topic': 'orderBookApi:BTC-USD_5'}
'''