import requests

""" Base session for Bluelink """
class Bluelink(requests.Session):
    def __init__(self, loginID, password, refreshAccessToken=True):
        from classes.vehicle import SSLAdapter
        from headers.default_headers import DEFAULT_HEADERS

        super().__init__()
        self.mount('https://', SSLAdapter()) # enable legacy ssl

        self.headers.update(DEFAULT_HEADERS) # add default headers

        # Setting to refresh access token every ~23 hours
        self.refresh = refreshAccessToken

        self.selectedVehicle = None
        self.accessToken = None
        self.vehicles = {}

        self.login(loginID, password) # login when initzalized
    
    """ Login to grab access token, and find vehicles (bool)"""
    def login(self, loginID, password, createVehicles=True) -> bool:
        headers = {'Referer': 'https://mybluelink.ca/login'}

        payload = {
            'loginId': loginID, 
            'password': password
        }

        # Get needed access token for all API requests by logging in.
        data = self.post(
            url='https://mybluelink.ca/tods/api/v2/login',
            json=payload,
            headers=headers
        ).json()
        
        self.accessToken = data['result']['token']['accessToken'] 

        if createVehicles:
            self.createVehicles()

        return True
    
    """ Get Pauth from correct pin, for API """
    def verifyPIN(self, pin: str, referer: str) -> str:
        cookie = self.cookies.get_dict()['dtCookie']
        headers = {
            'accessToken': self.accessToken,
            'Referer': referer,
            'Cookie': f'dtcookie={cookie};'
        }

        payload = {'pin': pin}

        # Get pAuth
        response = self.post(
            url='https://mybluelink.ca/tods/api/vrfypin',
            headers=headers,
            json=payload,
        )
        
        pAuth = response.json()['result']['pAuth']

        return pAuth
    
    """ Get all vehicles + selected vehicle, and create all Vehicle classes """
    def createVehicles(self) -> bool:
        from classes.vehicle import Vehicle

        # Grab default/selected vehicle
        selectedVehicle = self.post(
            url='https://mybluelink.ca/tods/api/v2/myvehicle',
            headers={
                'Accesstoken': self.accessToken,
                'Referer': 'https://mybluelink.ca/login'
            }
        ).json()['result']['selectedVehicle']['vehicle']

        # Create vehicle class for selected vehicle.
        self.selectedVehicle = Vehicle(
            selectedVehicle['nickName'].lower(), # watch for case on 2nd N
            selectedVehicle['vehicleId'], # watch for case on d
            selected=True,
            bluelinkSession=self
        )

        # Grab all vehicles in bluelink account
        vehicles = self.post(
            url="https://mybluelink.ca/tods/api/vhcllst",
            headers={
                'Accesstoken': self.accessToken,
                'Referer': 'https://mybluelink.ca/login'
            }
        ).json()['result']['vehicles']

        # Create a list of Vehicle classes for all vehicles in bluelink account
        for vehicle in vehicles:
            nickname = vehicle['nickName'].lower()
            id = vehicle['vehicleId']
            self.vehicles[nickname] = Vehicle(nickname, id, selected=False, bluelinkSession=self)
