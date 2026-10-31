from teaching_devices.models import DeviceStatusChangedEventArgs


class DeviceAuditLogger:
    def __init__(self) -> None:
        self._entries: list[str] = []

    @property
    def entries(self) -> tuple[str, ...]:  
        return tuple(self._entries)

    def handle_status_changed(self, sender: object, e: DeviceStatusChangedEventArgs) -> None:
        self._entries.append(f"{e.changed_at}: {e.device_id}, {e.old_status} -> {e.new_status}")
