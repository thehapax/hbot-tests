import json
from os import pathconf_names
import aiohttp, asyncio
from aiohttp.client import ClientSession
from utils import get_status_msg
import pprint
from decimal import Decimal
from btseauth_spot import BTSE_Endpoint, make_headers
from constants import *
from async_utils import *

pp = pprint.PrettyPrinter(indent=4)

from typing import (
    Any,
    Dict,
    List,
    Optional,
    AsyncIterable,
)

class BtseEx():
    def __init__(self):
        super().__init__()
        self._client = None
        self.BTSE_Endpoint = 'https://testapi.btse.io/spot'
        self.REST_URL = 'https://testapi.btse.io/spot'
        self.API_CALL_TIMEOUT = 10.0


    def get_orderids(self, result):
        ids = []
        for r in result:
            oid = r['orderID']
            ids.append(oid)
        print("\n\n Getting order ids:")
        print(ids)
        print("\n")
        return ids
    
    async def on_request_start(session, trace_config_ctx, params):
        print("Starting request")
        trace_config_ctx.start = asyncio.get_event_loop().time()

    async def on_request_end(session, trace_config_ctx, params):
        print("Ending request")
        elapsed = asyncio.get_event_loop().time() - trace_config_ctx.start
        print("Request took {}".format(elapsed))

    trace_config = aiohttp.TraceConfig()
    trace_config.on_request_start.append(on_request_start)
    trace_config.on_request_end.append(on_request_end)

    async def _http_client(self) -> aiohttp.ClientSession:
        """
        :returns Shared client session instance
        """
        if self._client is None:
            self._client = aiohttp.ClientSession()
        return self._client
    
    '''
    async def _api_request(self, 
                             http_method: str, 
                             path_url: str = None,
                             url: str = None, 
                             params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:

        assert path_url is not None or url is not None
        url = f"{self.BTSE_Endpoint}{path_url}" if url is None else url
#        data_str = '' if params is None else json.dumps(params)
        data_str = params # only for open orders
        headers = make_headers(path_url, '') # only for open orders
        client = await self._http_client()
        async with client.request(http_method, url=url, params=data_str, headers=headers) as response:
            data = await response.json()
            if response.status != 200:
                raise IOError(f"Error fetching data from {url}. HTTP status is {response.status}. {data}")
            print("\nOpen Orders - Parsed:")
            pp.pprint(data)
        await client.close()
        return data
    '''
    
    async def close_http(self):
        client = await self._http_client()
        await client.close()
        
        
    async def _api_request(self,
                           method: str, 
                           path: str = None, 
                           params: Optional[Dict[str, Any]] = {},
                           is_auth_required: bool = False) -> Dict[str, Any]:
        
        if is_auth_required:
            print("Auth is Required")
        prefix = '/api/v3.2/'
        path_url = prefix + path
        print(f'path url : {path_url}')
        url = f"{self.REST_URL}{path_url}"
        print(f"inside _api_request FULL URL : {url}")
        headers = make_headers(path_url, '')
        client = await self._http_client()

        try:
            if method == "get":
                print(f"\n INSIDE CLIENT.GET: url: {url} params: {params}\n")
                async with client.get(url, params=params, headers=headers) as response:
                    result = await response.text()
                    print(f"\n GET response: {result}")
                    
            elif method == "post": 
                jsond= json.dumps(params)
                headers = make_headers(path_url, jsond)
                print(f"\n INSIDE CLIENT.POST: url: {url}, json: {jsond}, headers: {headers}\n")
                # tricky - post uses json=params, header uses json.dumps(params)
                # hbot code uses client.request
                #async with client.request('post', url=url, json=jsond, headers=headers) as response:

                async with client.post(url, json=params, headers=headers) as response:
                    result = await response.text()
                    print(f"\n POST response: {result}")
                    
            elif method == "delete": # client.delete in hbot code
                print(f"\n INSIDE DELETE order. {url}, params: {params}, headers: {headers}\n")
                #async with client.delete(url, params=params, headers=headers) as response:
                async with client.request('delete', url=url, params=params, headers=headers) as response:
                    result = await response.text()
                    print(f"\n DELETE response: {result}")

            else:
                raise NotImplementedError
            
            # print(f'Result : {result}\n')
            parsed_response = json.loads(result)
            
        except Exception as e:
            raise IOError(f"Error parsing data from {url}. Error: {str(e)}")
        if response.status != 200:
            raise IOError(f"Error fetching data from {url}. HTTP status is {response.status}. "
                          f"Message: {parsed_response}")
        print(f"REQUEST: {method} {path_url} {params}")
        #print(f"RESPONSE: {parsed_response}")
        return parsed_response
            

    async def open_orders(self, path, params):
        '''
        Specifying which symbols are required or else 400 error will be thrown 
        can also use params as passed in by paramter
        '''
        # can this work with "post" and no params to get all open orders?
        result = await self._api_request(method='get', 
                                         path=path, 
                                         params=params,
                                         is_auth_required=True)
        # await self.close_http()
        return result

    async def update_trading_rules(self, params):
            print("inside _update_trading_rules in BtseExchange")
            # params={'symbol':'BTC-USDT'} ###### ADD TEMPORARY
            #params = {} # get all markets
            market_info = await self._api_request(method="get", 
                                                  path="market_summary", 
                                                  params=params, 
                                                  is_auth_required=False)
            # market_info = await self._api_request(method="get", path="market_summary")
            print(market_info)



    async def limit_order(self, path, params):
        result = await self._api_request(method='post', 
                                         path=path, 
                                         params=params,
                                         is_auth_required=True)
        # await self.close_http()
        return result
        
    async def delete_order(self, path, params):
        result = await self._api_request(method='delete', 
                                         path=path, 
                                         params=params,
                                         is_auth_required=True)
        # await self.close_http()
        return result


    '''
    async def limit_order(self, url, params, headers):
        client = await self._http_client(headers)
        try:
            response = await client.post(url, json=params, headers=headers)
            r = await response.text()
            print("LIMIT ORDER RESPONSE from client: " + r + "\n")
            parsed = json.loads(await response.text())
            print(f'\nLIMIT ORDER Parsed:\n {parsed}')
            if type(parsed) == list:
                code = parsed[0]['status']
                msg = get_status_msg(code)
                print(f'\nLimit Order Status Message: {msg}')
            else:   # error dict returned, get actual error message and return
                msg = parsed['message']
        except Exception as e:
            print(f'Exception: {e}')
        finally:
            await client.close()
    '''

    # old version
    async def del_order(self, url, params, headers):
        client = await self._http_client()
        try:
            async with client.delete(url, params=params, headers=headers) as response:
                print(await response.text())
                parsed = json.loads(await response.text())
                print(f'\nParsed:\n {parsed}')
                if type(parsed) == list:
                    code = parsed[0]['status']
                    msg = get_status_msg(code)
                    print(f'Status Message: {msg}')
                else:   # error dict returned, get actual error message and return
                    msg = parsed['message']
                return msg
        except Exception as e:
            print(e)
        finally:
            await client.close()

'''
    async def run(self):
        print(f'PARAMS: {open_order_params}\n')
        
        headers = make_headers(open_path, '')
        print("get open orders 1")
        result = await safe_gather(self._api_request('get', path_url=open_path, data=open_order_params))
'''