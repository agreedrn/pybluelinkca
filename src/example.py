import os
from classes.bluelink import Bluelink
import dotenv

# Define login_id, password, and your pin to use through your method of choosing
dotenv.load_dotenv()

LOGIN_ID = os.environ['loginID']
PASSWORD = os.environ['password']
PIN = os.environ['PIN']

# Create a bluelink session
session = Bluelink(LOGIN_ID, PASSWORD)

"""
session.selectedVehicle contains your default vehicle in bluelink
    - Available functions include:
        - lockOrUnlock(PIN, intent) -- intent = Literal['LOCK', 'UNLOCK']
        - session.selectedVehicle.enginePresets[settingNAME] -- engine presets in bluelink, returns a CarSetting() (src/classes/dataclasses/engine_presets.py)
        - startEngine(PIN, preset=None) -- will default to default set preset in bluelink account
            - you are able to use a custom one, either gotten from session.selectedVehicle.enginePresets[settingNAME]
                - or a custom made class of CarSetting() in src/classes/dataclasses/engine_presets.py 
                    - units are funky here, unknown ones, will create a easier way in the *future*
session.vehicles contains all vehicles in bluelink. Find one using session.vehicles[VEHICLE_NICKNAME]
    - Available functions are the same after one vehicle is defined.
    - e.g. session.vehicles[VEHICLE_NICKNAME].startEngine(PIN)
* Functions will return True if successful.
"""

# Select the vehicle
vehicle = session.selectedVehicle

print(vehicle.enginePresets.presetClasses)

# # Locking the vehicle
# locked = vehicle.lockOrUnlock(PIN, intent="LOCK")

# # Check if locking function returned True, if lock suceeded.
# if locked:
#     print(f"{vehicle.vehicleNickName} successfully locked.")

session.close() # make sure to end the session



