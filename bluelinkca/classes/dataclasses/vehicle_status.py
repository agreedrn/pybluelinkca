from dataclasses import dataclass
from dataclass_wizard import JSONSerializable, property_wizard
from typing import Optional


@dataclass
class ApiTransaction(JSONSerializable, metaclass=property_wizard):
    apiCode: str
    apiStartDate: str
    apiEndDate: str
    apiResult: str
    apiStatusCode: str


@dataclass
class DoorOpenStatus(JSONSerializable, metaclass=property_wizard):
    frontLeft: int
    frontRight: int
    backLeft: int
    backRight: int


@dataclass
class AirTemp(JSONSerializable, metaclass=property_wizard):
    value: str
    unit: int


@dataclass
class DistanceToEmpty(JSONSerializable, metaclass=property_wizard):
    value: float
    unit: int


@dataclass
class TirePressureLamp(JSONSerializable, metaclass=property_wizard):
    tirePressureLampAll: int

@dataclass
class BatSignalReferenceValue:
    batWarning: int

@dataclass
class Battery(JSONSerializable, metaclass=property_wizard):
    batSoc: int
    sjbDeliveryMode: int
    batSignalReferenceValue: BatSignalReferenceValue
    powerAutoCutMode: int

@dataclass
class SeatHeaterVentInfo(JSONSerializable, metaclass=property_wizard):
    drvSeatHeatState: int
    astSeatHeatState: int
    rlSeatHeatState: int
    rrSeatHeatState: int


@dataclass
class HeadLampStatus(JSONSerializable, metaclass=property_wizard):
    headLampStatus: bool
    leftLowLamp: bool
    rightLowLamp: bool
    leftHighLamp: bool
    rightHighLamp: bool
    leftBifuncLamp: bool
    rightBifuncLamp: bool


@dataclass
class StopLampStatus(JSONSerializable, metaclass=property_wizard):
    leftLamp: bool
    rightLamp: bool


@dataclass
class TurnSignalLampStatus(JSONSerializable, metaclass=property_wizard):
    leftFrontLamp: bool
    rightFrontLamp: bool
    leftRearLamp: bool
    rightRearLamp: bool


@dataclass
class LampWireStatus(JSONSerializable, metaclass=property_wizard):
    headLamp: HeadLampStatus
    stopLamp: StopLampStatus
    turnSignalLamp: TurnSignalLampStatus


@dataclass
class VehicleStatus(JSONSerializable, metaclass=property_wizard):
    lastStatusDate: str
    airCtrlOn: bool
    engine: bool
    doorLock: bool
    doorOpen: DoorOpenStatus
    trunkOpen: bool
    airTempUnit: str
    airTemp: AirTemp
    defrost: bool
    lowFuelLight: bool
    acc: bool
    hoodOpen: bool
    transCond: bool
    dte: DistanceToEmpty
    tirePressureLamp: TirePressureLamp
    battery: Battery
    remoteIgnition: bool
    seatHeaterVentInfo: SeatHeaterVentInfo
    sleepModeCheck: bool
    lampWireStatus: LampWireStatus
    smartKeyBatteryWarning: bool
    fuelLevel: int
    washerFluidStatus: bool
    breakOilStatus: bool
    engineOilStatus: bool
    engineRuntime: Optional[dict] = None
    windowOpen: Optional[dict] = None


@dataclass
class ResponseHeader(JSONSerializable, metaclass=property_wizard):
    responseCode: int
    responseDesc: str


@dataclass
class Result(JSONSerializable, metaclass=property_wizard):
    transaction: ApiTransaction
    vehicle: VehicleStatus

@dataclass
class ApiResponse(JSONSerializable, metaclass=property_wizard):
    responseHeader: ResponseHeader
    result: Result

"""

response = ApiResponse.from_dict(data)

"""
