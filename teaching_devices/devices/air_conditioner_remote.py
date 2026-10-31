from teaching_devices.devices.teaching_device import TeachingDevice
from teaching_devices.models import AlertSeverity


class AirConditionerRemote(TeachingDevice):
    def __init__(self, device_id: str, name: str, assigned_room: str) -> None:
        super().__init__(device_id, name)
        self._assigned_room = assigned_room
        self._is_responsive = True

    @property
    def assigned_room(self) -> str:
        return self._assigned_room

    @property
    def is_responsive(self) -> bool:
        return self._is_responsive

    def update_response_state(self, is_responsive: bool) -> None:
        was_responsive = self._is_responsive
        self._is_responsive = is_responsive
        if was_responsive and not is_responsive:  
            self._raise_alert(
                f"Điều hòa phòng {self._assigned_room} không phản hồi", AlertSeverity.CRITICAL
            )
