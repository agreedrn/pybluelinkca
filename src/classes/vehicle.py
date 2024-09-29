import ssl
import time
from requests.adapters import HTTPAdapter
import classes.bluelink as bluelink

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
    def __init__(self, vehicleNickName: str, vehicleID: str, selected: bool, bluelinkSession: bluelink.Bluelink):
        self.vehicleNickName = vehicleNickName
        self.vehicleID = vehicleID
        self.selected = selected
        self.bluelink = bluelinkSession
    
    def __str__(self) -> str:
        return f'{self.vehicleNickName}: {self.vehicleID}: {self.selected}'
    
    def lock(self, pin) -> bool:
        print("Lock function started...")

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

        # Send lock request
        transactionID = self.bluelink.post(
            url='https://mybluelink.ca/tods/api/drlck',
            headers=headers,
            json=payload
        ).headers.get('Transactionid')
        headers['Transactionid'] = transactionID
        
        # Poll for lock status
        while True:
            print("Polling lock status...")  # Add logging for status polling
            status_response = self.bluelink.post(
                url='https://mybluelink.ca/tods/api/rmtsts',
                headers=headers,
            )
            
            print(f"Status response: {status_response.content}")
            status = status_response.json()['result']

            # Check if the transaction is still ongoing
            if status['transaction']['apiStatusCode'] == 'null':
                print("Lock transaction still in progress...")
                time.sleep(11)
                continue

            # Check if the door is locked and return True
            if status['vehicle']['doorLock']:
                print("Successfully locked.")  # Logging success
                return True

            # If door is not locked, break the loop and return False
            print("Failed to lock.")  # Logging failure
            return False