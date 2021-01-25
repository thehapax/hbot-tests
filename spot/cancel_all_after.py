import socket
import requests
import json
from btseauth_spot import BTSE_Endpoint, make_headers


path = '/api/v3.2/order/cancelAllAfter'

headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json;charset=UTF-8'
}

# timeout in ms, 60000 = 60 seconds = 1 minute
cancel_all_after_form = { "timeout": 60 } 

r = requests.post(BTSE_Endpoint + path, 
                  json=cancel_all_after_form,
                  headers=make_headers(path, json.dumps(cancel_all_after_form)))

print("Cancel all response:")
print(len(r.text))
print(r.text)

'''
# requests on success does not provide a response
# use open orders to check if all orders are closed.

from the docs: 
https://www.btse.com/apiexplorer/spot/?python#cancelallafterorders

200 Response 

{
  "body": {},
  "statusCode": "100",
  "statusCodeValue": 0
}

'''