from __future__ import annotations

from typing import Iterable

from teaching_devices.devices import TeachingDevice
from teaching_devices.subscribers import (
    ConsoleNotificationService,
    DeviceAuditLogger,
    MaintenanceService,
)


class DeviceMonitoringCoordinator:

    def __init__(self, devices: Iterable[TeachingDevice],
                 notification_service: ConsoleNotificationService,
                 audit_logger: DeviceAuditLogger,
                 maintenance_service: MaintenanceService) -> None:
        self._devices: list[TeachingDevice] = list(devices)
        self._notification = notification_service
        self._audit = audit_logger
        self._maintenance = maintenance_service
        self._subscribed = False

    def subscribe(self) -> None:
        if self._subscribed:  
            return
        for d in self._devices:
            d.status_changed += self._audit.handle_status_changed
            d.alert_raised += self._notification.handle_alert
            d.alert_raised += self._maintenance.handle_critical_alert
        self._subscribed = True

    def unsubscribe(self) -> None:
        if not self._subscribed:
            return
        for d in self._devices:
            d.status_changed -= self._audit.handle_status_changed
            d.alert_raised -= self._notification.handle_alert
            d.alert_raised -= self._maintenance.handle_critical_alert
        self._subscribed = False

    def dispose(self) -> None:
        self.unsubscribe()

    def __enter__(self) -> "DeviceMonitoringCoordinator":
        self.subscribe()
        return self

    def __exit__(self, *exc) -> None:
        self.dispose()
