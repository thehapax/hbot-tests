import hashlib
import hmac
import time
import os
from typing import (
    Dict,
)

from requests import api
# works on testnet and production

#Production
api_key = os.environ['BTSE_API_KEY']
api_pass = os.environ['BTSE_SECRET_KEY']

# production
#BTSE_Endpoint = 'https://api.btse.com/spot'
#BTSE_WSEndpoint = 'wss://ws.btse.com' # old endpoint

# new endpoint as of 19 Jan 2021 wss://ws.btse.com/ws/spot 


# Testnet
BTSE_WSEndpoint = 'wss://testws.btse.io'
BTSE_Endpoint = 'https://testapi.btse.io/spot'


# websocket full url 
spot_wss = 'wss://testws.btse.io/spotWS'

#testnet tradingkey
#api_key = os.environ['BTSE_API_KEY']
#api_pass = os.environ['BTSE_SECRET_KEY']


# API Keys
keypair = {
    'API-KEY': api_key,
    'API-PASSPHRASE': api_pass
}

secret_key = api_pass
apikey = api_key

#print("Keypair:")
#print(keypair)


_last_tracking_nonce: int = 0

def get_tracking_nonce() -> str:
    global _last_tracking_nonce
    nonce = int(time.time() * 1000)
    _last_tracking_nonce = nonce if nonce > _last_tracking_nonce else _last_tracking_nonce + 1
    return str(_last_tracking_nonce)


def get_headers(path_url: str, data: str = "") -> Dict[str, any]:
    """
    Generates authentication headers required by btse
    :param path_url: e.g. "/accounts"
    :param data: request payload
    :return: a dictionary of auth headers
    """
    print("******* INSIDE GET HEADERS *******")
    # print(f'\n SECRET KEY : {secret_key}, API-KEY : {apikey} ')
    #api_secret: bytes = bytes(secret_key, 'latin-1')
    #api_key: bytes = bytes(apikey, 'latin-1')
    
    nonce = get_tracking_nonce()
    print(f'\nget_tracking_nonce: {nonce}')
    
    message = path_url + nonce + data
    print(f'MESSAGE: {message}')
    
    # bheaders = {}
    signature = hmac.new(
        bytes(secret_key, 'latin-1'),
        msg=bytes(message, 'latin-1'),
        digestmod=hashlib.sha384
    ).hexdigest()

    headers = {
        'btse-api': api_key,
        'btse-nonce': nonce,
        'btse-sign': signature,
        'Accept': 'application/json;charset=UTF-8',
        'Content-Type': 'application/json',
    }
    return headers


##Make Signature headers
def make_headers(path: str, data: str="") -> Dict[str, any]:
    nonce = str(int(time.time()*1000))
    #print("nonce:" + nonce)
    message = path + nonce + data
    print(f'make_headers - MESSAGE: {message}')
    headers = {}
    passph = keypair['API-PASSPHRASE']
    #print(f'api-pass: {passph}')
    
    signature = hmac.new(
        bytes(keypair['API-PASSPHRASE'], 'latin-1'),
        msg=bytes(message, 'latin-1'),
        digestmod=hashlib.sha384
    ).hexdigest()
    
    headers = {
        'btse-api':keypair['API-KEY'],
        'btse-nonce':nonce,
        'btse-sign':signature,
        'Accept': 'application/json;charset=UTF-8',
        'Content-Type': 'application/json',
    }
#    print(headers)
    return headers

def gen_auth(api_key, secret_key, path='/spotWS'):
    btsenonce = str(int(time.time()*1000))
    path = path + btsenonce + ''
    signature = hmac.new(
        bytes(secret_key, 'latin-1'),
        msg=bytes(path, 'latin-1'),
        digestmod=hashlib.sha384
    ).hexdigest()
    auth_payload = {
        'op': 'authKeyExpires',
        'args': [api_key, btsenonce, signature + ""]
    }
    return auth_payload    
