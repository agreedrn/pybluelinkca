from dataclasses import dataclass
from dataclass_wizard import DataClassJSONMixin
from typing import Optional


@dataclass
class ApiTransaction(DataClassJSONMixin):
    apiCode: str
    apiStartDate: str
    apiEndDate: str
    apiResult: str
    apiStatusCode: str


@dataclass
class DoorOpenStatus(DataClassJSONMixin):
    frontLeft: int
    frontRight: int
    backLeft: int
    backRight: int


@dataclass
class AirTemp(DataClassJSONMixin):
    value: str
    unit: int


@dataclass
class DistanceToEmpty(DataClassJSONMixin):
    value: float
    unit: int


@dataclass
class TirePressureLamp(DataClassJSONMixin):
    tirePressureLampAll: int


@dataclass
class Battery(DataClassJSONMixin):
    batSoc: int
    sjbDeliveryMode: int
    batWarning: int
    powerAutoCutMode: int


@dataclass
class SeatHeaterVentInfo(DataClassJSONMixin):
    drvSeatHeatState: int
    astSeatHeatState: int
    rlSeatHeatState: int
    rrSeatHeatState: int


@dataclass
class HeadLampStatus(DataClassJSONMixin):
    headLampStatus: bool
    leftLowLamp: bool
    rightLowLamp: bool
    leftHighLamp: bool
    rightHighLamp: bool
    leftBifuncLamp: bool
    rightBifuncLamp: bool


@dataclass
class StopLampStatus(DataClassJSONMixin):
    leftLamp: bool
    rightLamp: bool


@dataclass
class TurnSignalLampStatus(DataClassJSONMixin):
    leftFrontLamp: bool
    rightFrontLamp: bool
    leftRearLamp: bool
    rightRearLamp: bool


@dataclass
class LampWireStatus(DataClassJSONMixin):
    headLamp: HeadLampStatus
    stopLamp: StopLampStatus
    turnSignalLamp: TurnSignalLampStatus


@dataclass
class Vehicle(DataClassJSONMixin):
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
    windowOpen: Optional[dict]
    smartKeyBatteryWarning: bool
    fuelLevel: int
    washerFluidStatus: bool
    breakOilStatus: bool
    engineOilStatus: bool
    engineRuntime: Optional[dict]


@dataclass
class ResponseHeader(DataClassJSONMixin):
    responseCode: int
    responseDesc: str


@dataclass
class Result(DataClassJSONMixin):
    transaction: ApiTransaction
    vehicle: Vehicle


@dataclass
class ApiResponse(DataClassJSONMixin):
    responseHeader: ResponseHeader
    result: Result

"""

response = ApiResponse.from_dict(data)

"""
