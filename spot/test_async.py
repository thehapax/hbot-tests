import aiohttp
import asyncio
import logging
import pprint
import time

pp = pprint.PrettyPrinter(indent=4)

BASE_URL = 'https://testapi.btse.io/spot/api/v3.2/'
trading_pair = 'BTC-USD'
url = f'{BASE_URL}orderbook/L2'
#&symbol={trading_pair}'
TICKER_URL = 'https://testapi.btse.io/spot/api/v3.2/price?symbol=BTC-USD'

# f"{constants.REST_URL}/spot/api/v3.2/orderbook/L2&symbol={trading_pair}"

# https://testapi.btse.io/spot/api/v3.2/orderbook/L2&symbol=BTC-USD
print(url)

async def safe_gather(*args, **kwargs):
    try:
        return await asyncio.gather(*args, **kwargs)
    except Exception as e:
        logging.getLogger(__name__).debug(f"Unhandled error in background task: {str(e)}", exc_info=True)
        raise

async def get_ticker():
    async with aiohttp.ClientSession() as client:
        params = {'symbol': 'BTC-USD'}
        response = await client.get(url, params=params)
        #data: List[Dict[str, Any]] = await safe_gather(response.json())
        if response.status != 200:
            print("error in response")
        data: List[Dict[str, Any]] = await response.json()
        pp.pprint(data)
        return data

def main():
    '''
    print(time.time())
    ev_loop: asyncio.BaseEventLoop = asyncio.get_event_loop()
    ev_loop.run_until_complete(asyncio.sleep(2.0))
    print("end of wait")
    print(time.time())
    '''
    
    # test get ticker
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_ticker())
    loop.close()
    

if __name__ == '__main__':
    main()