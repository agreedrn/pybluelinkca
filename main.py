import requests
import ssl
import time
import json
import dotenv
import os
from requests.adapters import HTTPAdapter
from bluelink import Bluelink

dotenv.load_dotenv() # load env vars from .env

# !-----  grabbed off internet, to fix legacy ssl problem with mybluelink.ca ------!
class SSLAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = ssl.create_default_context()
        # Enable unsafe legacy renegotiation
        context.options |= 0x4  # OP_LEGACY_SERVER_CONNECT
        kwargs['ssl_context'] = context
        return super().init_poolmanager(*args, **kwargs)

''' vehicle controls '''
class Vehicle():
    def __init__(self, vehicleNickName: str, vehicleID: str, selected: bool, bluelinkSession: Bluelink):
        self.vehicleNickName = vehicleNickName
        self.vehicleID = vehicleID
        self.selected = selected
        self.bluelink = bluelinkSession
    
    def __str__(self) -> str:
        return f'{self.vehicleNickName}: {self.vehicleID}: {self.selected}'
    
    # def lock(self) -> bool:
    #     headers = {
    #         'Accesstoken' = self.bluelink.accessToken,
    #         'Vehicleid'
    #     }

    #     self.bluelink.post(url='')

loginID = os.environ['loginID']
password = os.environ['password']

# create session for mybluelink
session = Bluelink(loginID, password)

session.close()


