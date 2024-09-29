import requests

""" create mybluelink.ca session """
class Bluelink(requests.Session):
    def __init__(self, loginID, password):
        from classes.vehicle import SSLAdapter
        from classes.headers.default_headers import DEFAULT_HEADERS

        super().__init__()
        self.mount('https://', SSLAdapter()) # enable legacy ssl

        self.headers.update(DEFAULT_HEADERS)

        self.selectedVehicle = None
        self.accessToken = None
        self.vehicles = {}

        self.login(loginID, password)
    
    def login(self, loginID, password) -> bool:
        self.get('https://mybluelink.ca/login') # go to login page

        headers = { # extra func specific headers
            'Referer': 'https://mybluelink.ca/login'
        }

        payload = {
            'loginId': loginID, 
            'password': password
        }

        data = self.post(url='https://mybluelink.ca/tods/api/v2/login', json=payload, headers=headers).json()

        self.accessToken = data['result']['token']['accessToken']

        self.createVehicles()
        return True
    
    def verifyPIN(self, pin: str, referer: str) -> str:
        cookie = self.cookies.get_dict()['dtCookie']
        headers = {
            'accessToken': self.accessToken,
            'Referer': referer,
            'Cookie': f'dtcookie={cookie};'
        }

        payload = {
            'pin': pin
        }

        data = self.post(
            url='https://mybluelink.ca/tods/api/vrfypin',
            headers=headers,
            json=payload,
        )
        
        pAuth = data.json()['result']['pAuth']

        return pAuth
    
    def createVehicles(self) -> bool:
        from classes.vehicle import Vehicle

        selectedVehicle = self.post(url='https://mybluelink.ca/tods/api/v2/myvehicle',
                                    headers={
                                        'Accesstoken': self.accessToken,
                                        'Referer': 'https://mybluelink.ca/login'
                                    }).json()
        selectedVehicle = selectedVehicle['result']['selectedVehicle']['vehicle']['vehicleId']

        vehicles = self.post(url="https://mybluelink.ca/tods/api/vhcllst",
                             headers={
                                 'Accesstoken': self.accessToken,
                                 'Referer': 'https://mybluelink.ca/login'
                            }).json()
        vehicles = vehicles['result']['vehicles']

        for vehicle in vehicles:
            nickname = vehicle['nickName'].lower()
            id = vehicle['vehicleId']

            if id == selectedVehicle:
                vehicleClass = Vehicle(nickname, id, selected=True, bluelinkSession=self)
                self.selectedVehicle, self.vehicles[nickname] = vehicleClass, vehicleClass
            else:
                self.vehicles[nickname] = Vehicle(nickname, id, selected=False, bluelinkSession=self)
