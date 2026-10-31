from typing import Callable

from teaching_devices.models import DeviceAlertEventArgs

AlertFilter = Callable[[DeviceAlertEventArgs], bool]


class FilteredAlertSubscriber:
    def __init__(self, alert_filter: AlertFilter,
                 action: Callable[[DeviceAlertEventArgs], None]) -> None:
        self._filter = alert_filter
        self._action = action

    def handle_alert(self, sender: object, e: DeviceAlertEventArgs) -> None:
        if self._filter(e):
            self._action(e)
