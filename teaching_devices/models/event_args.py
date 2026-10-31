from dataclasses import dataclass
from datetime import datetime

from teaching_devices.models.enums import AlertSeverity, DeviceStatus


@dataclass(frozen=True)
class DeviceStatusChangedEventArgs:
    device_id: str
    old_status: DeviceStatus
    new_status: DeviceStatus
    changed_at: datetime


@dataclass(frozen=True)
class DeviceAlertEventArgs:
    device_id: str
    message: str
    severity: AlertSeverity
    occurred_at: datetime
