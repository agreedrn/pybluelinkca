from main import SSLAdapter, Vehicle
import requests
import json

""" create mybluelink.ca session """
class Bluelink(requests.Session):
    def __init__(self, loginID, password, PIN):
        super().__init__()
        self.mount('https://', SSLAdapter()) # enable legacy ssl
        self.headers.update({
            'Host': 'mybluelink.ca',
            'Origin': 'https://mybluelink.ca',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 OPR/112.0.0.0',
            'Content-Type': 'application/json;charset=UTF-8',
            'From': 'CWP',
            'Language': '0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Offset': '-4',    
        })
        self.selectedVehicle = None
        self.accessToken = None
        self.vehicles = None
        self.PIN = PIN
        self.login(loginID, password)
    
    def login(self, loginID, password) -> bool:
        self.get('https://mybluelink.ca/login') # go to login page

        headers = { # extra func specific headers
            'Referer': 'https://mybluelink.ca/login'
        }

        payload = json.dumps({
            'loginId': loginID, 
            'password': password
        })

        data = self.post(url='https://mybluelink.ca/tods/api/v2/login', data=payload, headers=headers).json()

        self.accessToken = data['result']['token']['accessToken']

        self.createVehicles()
        return True
    
    def createVehicles(self) -> bool:
        selectedVehicle = self.post(url='https://mybluelink.ca/tods/api/v2/myvehicle',
                                    headers={'Accesstoken': self.accessToken}).json()
        selectedVehicle = selectedVehicle['result']['selectedVehicle']['vehicle']['vehicleId']

        self.vehicles = {}

        vehicles = self.post(url="https://mybluelink.ca/tods/api/vhcllst",
                             headers={'Accesstoken': self.accessToken}).json()
        vehicles = vehicles['result']['vehicles']

        for vehicle in vehicles:
            nickname = vehicle['nickName']
            id = vehicle['vehicleId']
            vehicleClass = ''

            if id == selectedVehicle:
                vehicleClass = Vehicle(nickname, id, selected=True)
                self.selectedVehicle = vehicleClass
                self.vehicles[nickname] = Vehicle(nickname, id, selected=True, bluelinkSession=self)
            else:
                self.vehicles[nickname] = Vehicle(vehicle['nickName'], id, selected=False, bluelinkSession=self)
