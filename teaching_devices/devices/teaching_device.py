from __future__ import annotations

from abc import ABC
from datetime import datetime

from teaching_devices.events import Event, EventSubscription
from teaching_devices.models import (
    AlertSeverity,
    DeviceAlertEventArgs,
    DeviceStatus,
    DeviceStatusChangedEventArgs,
)


class TeachingDevice(ABC):

    def __init__(self, device_id: str, name: str) -> None:
        if type(self) is TeachingDevice:
            raise TypeError
        self._id = device_id
        self._name = name
        self._status = DeviceStatus.AVAILABLE
        self._status_changed: Event[DeviceStatusChangedEventArgs] = Event()
        self._alert_raised: Event[DeviceAlertEventArgs] = Event()

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def status(self) -> DeviceStatus:
        return self._status

    @property
    def status_changed(self) -> EventSubscription[DeviceStatusChangedEventArgs]:
        return self._status_changed.public

    @status_changed.setter
    def status_changed(self, value) -> None:
        if value is not self._status_changed.public:
            raise AttributeError

    @property
    def alert_raised(self) -> EventSubscription[DeviceAlertEventArgs]:
        return self._alert_raised.public

    @alert_raised.setter
    def alert_raised(self, value) -> None:
        if value is not self._alert_raised.public:
            raise AttributeError

    def change_status(self, new_status: DeviceStatus) -> None:
        if new_status == self._status:
            return 
        old_status = self._status
        self._status = new_status 
        self._on_status_changed(
            DeviceStatusChangedEventArgs(self._id, old_status, new_status, datetime.now())
        )

    def _raise_alert(self, message: str, severity: AlertSeverity) -> None:
        self._on_alert_raised(DeviceAlertEventArgs(self._id, message, severity, datetime.now()))

    def _on_status_changed(self, e: DeviceStatusChangedEventArgs) -> None:
        self._status_changed.invoke(self, e)

    def _on_alert_raised(self, e: DeviceAlertEventArgs) -> None:
        self._alert_raised.invoke(self, e)
