from enum import Enum

from pydantic import BaseModel


class FirmwareVersionType(str, Enum):
    DEV = "DEV"
    ALPHA = "ALPHA"
    BETA = "BETA"
    RC = "RC"
    STABLE = "STABLE"

    @staticmethod
    def from_value(firmware_value: int) -> "FirmwareVersionType":
        return {
            0: FirmwareVersionType.DEV,
            64: FirmwareVersionType.ALPHA,
            128: FirmwareVersionType.BETA,
            192: FirmwareVersionType.RC,
            255: FirmwareVersionType.STABLE,
        }[firmware_value]


class MavlinkVehicleType(str, Enum):
    MAV_TYPE_GENERIC = "Generic"
    MAV_TYPE_FIXED_WING = "Fixed Wing"
    MAV_TYPE_QUADROTOR = "Quadrotor"
    MAV_TYPE_COAXIAL = "Coaxial"
    MAV_TYPE_HELICOPTER = "Helicopter"
    MAV_TYPE_ANTENNA_TRACKER = "Antenna Tracker"
    MAV_TYPE_GCS = "Gcs"
    MAV_TYPE_AIRSHIP = "Airship"
    MAV_TYPE_FREE_BALLOON = "Free Balloon"
    MAV_TYPE_ROCKET = "Rocket"
    MAV_TYPE_GROUND_ROVER = "Ground Rover"
    MAV_TYPE_SURFACE_BOAT = "Surface Boat"
    MAV_TYPE_SUBMARINE = "Submarine"
    MAV_TYPE_HEXAROTOR = "Hexarotor"
    MAV_TYPE_OCTOROTOR = "Octorotor"
    MAV_TYPE_TRICOPTER = "Tricopter"
    MAV_TYPE_FLAPPING_WING = "Flapping Wing"
    MAV_TYPE_KITE = "Kite"
    MAV_TYPE_ONBOARD_CONTROLLER = "Onboard Controller"
    MAV_TYPE_VTOL_DUOROTOR = "Vtol (Duorotor)"
    MAV_TYPE_VTOL_QUADROTOR = "Vtol (Quadrotor)"
    MAV_TYPE_VTOL_TILTROTOR = "Vtol (Tiltrotor)"
    MAV_TYPE_VTOL_FIXEDROTOR = "Vtol (Fixedrotor)"
    MAV_TYPE_VTOL_TAILSITTER = "Vtol (Tailsitter)"
    MAV_TYPE_VTOL_RESERVED4 = "Vtol (Reserved4)"
    MAV_TYPE_VTOL_RESERVED5 = "Vtol (Reserved5)"
    MAV_TYPE_GIMBAL = "Gimbal"
    MAV_TYPE_ADSB = "Adsb"
    MAV_TYPE_PARAFOIL = "Parafoil"
    MAV_TYPE_DODECAROTOR = "Dodecarotor"
    MAV_TYPE_CAMERA = "Camera"
    MAV_TYPE_CHARGING_STATION = "Charging Station"
    MAV_TYPE_FLARM = "Flarm"
    MAV_TYPE_SERVO = "Servo"
    MAV_TYPE_ODID = "Odid"
    MAV_TYPE_DECAROTOR = "Decarotor"
    MAV_TYPE_BATTERY = "Battery"
    MAV_TYPE_PARACHUTE = "Parachute"
    MAV_TYPE_LOG = "Log"
    MAV_TYPE_OSD = "Osd"
    MAV_TYPE_IMU = "Imu"
    MAV_TYPE_GPS = "Gps"
    MAV_TYPE_WINCH = "Winch"


class FirmwareInfo(BaseModel):
    version: str
    type: FirmwareVersionType


class MavlinkMessageId(Enum):
    HEARTBEAT = 0
    AUTOPILOT_VERSION = 148
