from sensor_state_data import (
    BaseDeviceClass,
)

class ExtendedSensorDeviceClass(BaseDeviceClass):
    """Device class for additional sensors (compared to sensor-state-data)."""

    # Data channel
    CHANNEL = "channel"

    # Raw hex data
    RAW = "raw"

    # Text
    TEXT = "text"

    # Volume storage
    VOLUME_STORAGE = "volume_storage"

    # Direction
    DIRECTION = "direction"

    # Precipitation
    PRECIPITATION = "precipitation"

