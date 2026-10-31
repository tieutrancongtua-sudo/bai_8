from teaching_devices.models import AlertSeverity, DeviceAlertEventArgs


class MaintenanceService:
    def __init__(self) -> None:
        self._requests: list[str] = []

    @property
    def requests(self) -> tuple[str, ...]:
        return tuple(self._requests)

    def handle_critical_alert(self, sender: object, e: DeviceAlertEventArgs) -> None:
        if e.severity != AlertSeverity.CRITICAL:
            return
        self._requests.append(f"Maintenance request for {e.device_id}: {e.message}")
