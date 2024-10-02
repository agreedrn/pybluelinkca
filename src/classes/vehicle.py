import ssl
import time
import copy
from . import bluelink
from requests.adapters import HTTPAdapter
from typing import Literal
from .dataclasses.vehicle_status import ApiResponse, VehicleStatus
from .dataclasses.engine_presets import CarSetting, CarSettings

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
    
    """ Function to get all status arguments of the vehicle. GET FUNC NOT FULLY BUILT*"""
    def pollOrGetStatus(self, intent: Literal['POLL', 'GET'], headers=None) -> VehicleStatus:
        if intent == 'POLL':
            endpoint = 'rmsts'
        elif intent == 'GET':
            endpoint = ''
            headers = {}
        
        # Poll for status (every 11 seconds)
        while True:
            # Grab the status of the API request
            status_response = self.bluelink.post(
                url='https://mybluelink.ca/tods/api/rmtsts',
                headers=headers,
            )
            status = status_response.json()

            # Check if the transaction is still ongoing
            if status['result']['transaction']['apiStatusCode'] == 'null':
                time.sleep(11)
                continue
            elif status['result']['transaction']['apiStatusCode']== '200':
                status = ApiResponse.from_dict(status)
                return status.result.vehicle
    
    """ Function to lock/unlock the vehicle with specified PIN """
    def lockOrUnlock(self, pin: str, intent: Literal['LOCK', 'UNLOCK']) -> bool:
        referer = 'https://mybluelink.ca/remote/lock'
        headers = { 
            'Accesstoken': self.bluelink.accessToken,
            'Vehicleid': self.vehicleID,
            'Pauth': self.bluelink.verifyPIN(pin, referer),
            'Referer': referer
        }
        payload = {'pin': pin}

        # Select right API endpoint depending on if locking or unlocking
        endpoint = 'drulck' if intent == "UNLOCK" else 'drlck'

        # Send lock request
        transactionID = self.bluelink.post(
            url=f'https://mybluelink.ca/tods/api/{endpoint}',
            headers=headers,
            json=payload
        ).headers.get('Transactionid') # watch for case
        headers['Transactionid'] = transactionID # watch for case

        # Poll for status of car after API req. completed
        status = self.pollOrGetStatus(intent='POLL', headers=headers)

        # Confirm if API did its job, and end func (check if door is unlocked/locked)
        locking = False if intent == "UNLOCK" else True
        if status.doorLock == locking:
            return True
    
    def getEnginePresets(self) -> CarSettings:
        # Headers
        headers = {
            'Accesstoken': self.bluelink.accessToken,
            'Vehicleid': self.vehicleID,
            'Referer': 'https://mybluelink.ca/remote/start'
        }

        # Grab engine presets
        presets = self.bluelink.post(url='https://mybluelink.ca/tods/api/gtfvsttng', headers=headers)
        presets = presets.json()['result']

        # Find presets + default preset
        presetClasses = []
        defaultClass = None
        for preset in presets:
            # Create a new copy of the preset, without id and settingName (prep for start engine func)
            new_preset = copy.deepcopy(preset)
            del new_preset['id']
            del new_preset['settingName']

            preset['setting_json'] = new_preset

            print(preset)

            if preset['defaultFavorite']:
                defaultClass = CarSetting.from_dict(preset)
            presetClasses.append(CarSetting.from_dict(preset))
        
        # Return preset class
        return CarSettings(presetClasses, defaultClass)
    
    def startEngine(self, pin, preset: CarSetting | None) -> bool:
        # Grab default preset (if exists)
        presets = self.getEnginePresets()
        if presets.defaultPreset:
            preset = presets.defaultPreset
        else:
            raise RuntimeError('Your bluelink account does not contain a default preset.\nPlease either include a custom preset when calling this function, or set a default one in your bluelink account.')

        referer = 'https://mybluelink.ca/remote/start'

        # Headers
        headers = {
            'Accesstoken': self.bluelink.accessToken,
            'Pauth': self.bluelink.verifyPIN(pin, referer),
            'Vehicleid': self.vehicleID
        }

        # Payload
        payload = {
            'pin': pin,
            'setting': preset.setting_json
        }

        # Start the car + get Transactionid for polling
        transactionID = self.bluelink.post(
            url='https://mybluelink.ca/tods/api/rmtstrt',
            headers=headers,
            json=payload
        ).headers.get('Transactionid') # watch for case
        headers['Transactionid'] = transactionID # watch for case

        # Poll for start request status
        status = self.pollOrGetStatus(intent='POLL', headers=headers)

        # Quick check if engine is on and API did its job
        if status.engine:
            return True
