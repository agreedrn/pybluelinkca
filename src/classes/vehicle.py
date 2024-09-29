import ssl
import time
import classes.bluelink as bluelink
from requests.adapters import HTTPAdapter
from typing import Literal

# !-----  grabbed off internet, to fix legacy ssl problem with mybluelink.ca -----!
class SSLAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = ssl.create_default_context()
        # Enable unsafe legacy renegotiation
        context.options |= 0x4  # OP_LEGACY_SERVER_CONNECT
        kwargs['ssl_context'] = context
        return super().init_poolmanager(*args, **kwargs)

''' Vehicle information + functions for vehicle '''
class Vehicle():
    def __init__(self, vehicleNickName: str, vehicleID: str, selected: bool, bluelinkSession: bluelink.Bluelink):
        self.vehicleNickName = vehicleNickName
        self.vehicleID = vehicleID
        self.selected = selected
        self.bluelink = bluelinkSession
    
    def __str__(self) -> str:
        return f'{self.vehicleNickName}: {self.vehicleID}: {self.selected}'
    
    """ Function to lock/unlock the vehicle with specified PIN """
    def lockOrUnlock(self, pin: str, intent: Literal['LOCK', 'UNLOCK']) -> bool:
        referer = 'https://mybluelink.ca/remote/lock'
        headers = { 
            'Accesstoken': self.bluelink.accessToken,
            'Vehicleid': self.vehicleID,
            'Pauth': self.bluelink.verifyPIN(pin, referer),
            'Referer': referer
        }

        payload = {
            'pin': pin
        }

        # Select right API endpoint depending on if locking or unlocking
        endpoint = 'drulck' if intent == "UNLOCK" else 'drlck'

        # Send lock request
        transactionID = self.bluelink.post(
            url=f'https://mybluelink.ca/tods/api/{endpoint}',
            headers=headers,
            json=payload
        ).headers.get('Transactionid') # watch for case
        headers['Transactionid'] = transactionID # watch for case
        
        # Poll for lock status (every 11 seconds)
        while True:
            print("Polling lock status...")
            status_response = self.bluelink.post(
                url='https://mybluelink.ca/tods/api/rmtsts',
                headers=headers,
            )
            
            print(f"Status response: {status_response.content}")
            status = status_response.json()['result']

            # Check if the transaction is still ongoing
            if status['transaction']['apiStatusCode'] == 'null':
                print("Transaction still in progress...")
                time.sleep(11)
                continue

            locking = False if intent == "UNLOCK" else True
            # Check if the door is locked/unlocked (depending) and return True
            if status['vehicle'][f'doorLock'] == locking:
                print(f"Successfully {intent.lower()}ed.")
                return True