from teaching_devices.models import DeviceAlertEventArgs


class ConsoleNotificationService:
    def handle_alert(self, sender: object, e: DeviceAlertEventArgs) -> None:
        print(f"[{e.severity}] {e.device_id}: {e.message}")
