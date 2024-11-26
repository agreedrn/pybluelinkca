from dataclasses import dataclass
from dataclass_wizard import JSONSerializable, property_wizard
from typing import Optional

@dataclass
class AirTemp(JSONSerializable, metaclass=property_wizard):
    value: str
    unit: int

@dataclass
class SeatHeaterVentCMD(JSONSerializable, metaclass=property_wizard):
    drvSeatOptCmd: int
    astSeatOptCmd: int
    rlSeatOptCmd: int
    rrSeatOptCmd: int

@dataclass
class CarSetting(JSONSerializable, metaclass=property_wizard):
    id: int
    settingName: str
    airCtrl: int
    defrost: bool
    airTemp: AirTemp
    igniOnDuration: int
    heating1: int
    ims: int
    defaultFavorite: bool

    # setting dict, for req.
    setting_json: dict

    seatHeaterVentCMD: Optional[SeatHeaterVentCMD] = None

@dataclass
class CarSettings():
    presetClasses: dict
    defaultPreset: Optional[CarSetting] = None