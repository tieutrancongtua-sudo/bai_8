
from teaching_devices.models.enums import AlertSeverity
from teaching_devices.models.exceptions import InvalidDeviceReadingException


def validate_percent(device_id: str, value: int, what: str) -> None:
    if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value <= 100:
        raise InvalidDeviceReadingException(device_id, value, what)


def zone(level: int, warning_below: int) -> AlertSeverity:
    if level == 0:
        return AlertSeverity.CRITICAL
    if level < warning_below:
        return AlertSeverity.WARNING
    return AlertSeverity.INFORMATION
