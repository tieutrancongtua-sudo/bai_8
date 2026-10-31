from teaching_devices.devices.readings import validate_percent, zone
from teaching_devices.devices.teaching_device import TeachingDevice
from teaching_devices.models import AlertSeverity


class ProjectorRemote(TeachingDevice):
    WARNING_BELOW = 20

    def __init__(self, device_id: str, name: str, battery_level: int = 100) -> None:
        super().__init__(device_id, name)
        validate_percent(device_id, battery_level, "mức pin")
        self._battery_level = battery_level

    @property
    def battery_level(self) -> int:
        return self._battery_level

    def update_battery_level(self, new_level: int) -> None:
        validate_percent(self._id, new_level, "mức pin")  
        old_zone = zone(self._battery_level, self.WARNING_BELOW)
        new_zone = zone(new_level, self.WARNING_BELOW)
        self._battery_level = new_level
        if new_zone > old_zone:
            if new_zone == AlertSeverity.CRITICAL:
                self._raise_alert("Pin máy chiếu đã hết (0%)", AlertSeverity.CRITICAL)
            else:
                self._raise_alert(f"Pin máy chiếu thấp ({new_level}%)", AlertSeverity.WARNING)
