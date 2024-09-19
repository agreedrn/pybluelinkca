import requests
import ssl
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
import time
import json

class SSLAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = ssl.create_default_context()
        # Enable unsafe legacy renegotiation
        context.options |= 0x4  # OP_LEGACY_SERVER_CONNECT
        kwargs['ssl_context'] = context
        return super().init_poolmanager(*args, **kwargs)

# Create a session and mount the adapter
session = requests.Session()
session.mount('https://', SSLAdapter())

# Try to make the request
response = session.get('https://mybluelink.ca/login')

headers = {
    'Host': 'mybluelink.ca',
    'Origin': 'https://mybluelink.ca',
    'Referer': 'https://mybluelink.ca/login',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 OPR/112.0.0.0',
    'content-type': 'application/json;charset=UTF-8',
    'From': 'CWP',
    'Language': '0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'offset': '-4',
}

loginId = input('loginID: ')
password = input('password: ')

payload = json.dumps({
    'loginId': loginId, 
    'password': password
})
response = session.post(url='https://mybluelink.ca/tods/api/v2/login', data=payload, headers=headers)
print(response.content)
