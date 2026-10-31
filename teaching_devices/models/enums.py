from enum import Enum, IntEnum


class DeviceStatus(Enum):
    AVAILABLE = "Available"
    BORROWED = "Borrowed"
    UNDER_MAINTENANCE = "UnderMaintenance"

    def __str__(self) -> str:
        return self.value


class AlertSeverity(IntEnum):
    INFORMATION = 0
    WARNING = 1
    CRITICAL = 2

    def __str__(self) -> str:
        return self.name.capitalize()
