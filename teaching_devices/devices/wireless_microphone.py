from teaching_devices.devices.readings import validate_percent, zone
from teaching_devices.devices.teaching_device import TeachingDevice
from teaching_devices.models import AlertSeverity


class WirelessMicrophone(TeachingDevice):
    BATTERY_WARNING_BELOW = 30
    SIGNAL_WARNING_BELOW = 40

    def __init__(self, device_id: str, name: str,
                 battery_level: int = 100, signal_quality: int = 100) -> None:
        super().__init__(device_id, name)
        validate_percent(device_id, battery_level, "mức pin")
        validate_percent(device_id, signal_quality, "chất lượng tín hiệu")
        self._battery_level = battery_level
        self._signal_quality = signal_quality

    @property
    def battery_level(self) -> int:
        return self._battery_level

    @property
    def signal_quality(self) -> int:
        return self._signal_quality

    def update_battery_level(self, new_level: int) -> None:
        validate_percent(self._id, new_level, "mức pin")
        old_zone = zone(self._battery_level, self.BATTERY_WARNING_BELOW)
        new_zone = zone(new_level, self.BATTERY_WARNING_BELOW)
        self._battery_level = new_level
        if new_zone > old_zone:
            if new_zone == AlertSeverity.CRITICAL:
                self._raise_alert("Pin micro đã hết (0%)", AlertSeverity.CRITICAL)
            else:
                self._raise_alert(f"Pin micro thấp ({new_level}%)", AlertSeverity.WARNING)

    def update_signal_quality(self, new_quality: int) -> None:
        validate_percent(self._id, new_quality, "chất lượng tín hiệu")
        old_zone = zone(self._signal_quality, self.SIGNAL_WARNING_BELOW)
        new_zone = zone(new_quality, self.SIGNAL_WARNING_BELOW)
        self._signal_quality = new_quality
        if new_zone > old_zone:
            if new_zone == AlertSeverity.CRITICAL:
                self._raise_alert("Micro mất tín hiệu (0%)", AlertSeverity.CRITICAL)
            else:
                self._raise_alert(f"Tín hiệu micro yếu ({new_quality}%)", AlertSeverity.WARNING)
