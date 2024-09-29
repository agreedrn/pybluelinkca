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
    - Available functions include: lock(PIN), unlock(PIN), etc.
    - e.g. session.selectedVehicle.lock(PIN)
session.vehicles contains all vehicles in bluelink. Find one using session.vehicles[VEHICLE_NICKNAME]
    - Available functions are the same after one vehicle is defined.
    - e.g. session.vehicles[VEHICLE_NICKNAME].lock(PIN)
* Functions will return True if successful.
"""

vehicle = session.selectedVehicle

# unlocking the vehicle
vehicle.lockOrUnlock(PIN, intent="LOCK")

session.close() # make sure to end the session



