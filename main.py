
from teaching_devices.coordinator import DeviceMonitoringCoordinator
from teaching_devices.devices import AirConditionerRemote, ProjectorRemote, WirelessMicrophone
from teaching_devices.models import AlertSeverity, DeviceStatus, InvalidDeviceReadingException
from teaching_devices.subscribers import (
    ConsoleNotificationService,
    DeviceAuditLogger,
    FilteredAlertSubscriber,
    MaintenanceService,
)


def title(text: str) -> None:
    print(f"\n===== {text} =====")


def demo_status_changes(projector, mic, logger) -> None:
    title("1. Thay đổi trạng thái -> StatusChanged")
    projector.change_status(DeviceStatus.BORROWED)
    projector.change_status(DeviceStatus.BORROWED) 
    mic.change_status(DeviceStatus.UNDER_MAINTENANCE)

    for line in logger.entries:
        print(line)
    assert len(logger.entries) == 2
    assert projector.status == DeviceStatus.BORROWED  


def demo_projector_battery(projector, maintenance) -> None:
    title("2. Pin máy chiếu (cảnh báo dưới 20%, Critical khi 0%)")
    before = len(maintenance.requests)
    projector.update_battery_level(50)  
    projector.update_battery_level(15)  
    projector.update_battery_level(10)  
    projector.update_battery_level(0)   
    assert len(maintenance.requests) == before + 1


def demo_air_conditioner(ac, maintenance) -> None:
    title("3. Điều hòa không phản hồi")
    before = len(maintenance.requests)
    ac.update_response_state(False)  
    ac.update_response_state(False)  
    assert len(maintenance.requests) == before + 1


def demo_microphone(mic, maintenance) -> None:
    title("4. Micro: pin (<30%) và tín hiệu (<40%)")
    before = len(maintenance.requests)
    mic.update_battery_level(25)    
    mic.update_signal_quality(30)  
    mic.update_signal_quality(0)    
    assert len(maintenance.requests) == before + 1


def demo_invalid_reading(mic) -> None:
    title("5. Dữ liệu không hợp lệ")
    old_level = mic.battery_level
    try:
        mic.update_battery_level(150)
    except InvalidDeviceReadingException as ex:
        print(f"{ex} (device={ex.device_id}, value={ex.invalid_value})")
    else:
        raise AssertionError("phải ném InvalidDeviceReadingException")
    assert mic.battery_level == old_level  


def demo_encapsulation(projector) -> None:
    title("6. Bên ngoài không được tự phát sinh / gán đè event")
    assert not hasattr(projector.alert_raised, "invoke")
    try:
        projector.alert_raised = None
    except AttributeError as ex:
        print("Bị chặn:", ex)
    else:
        raise AssertionError("không được gán đè event")


def demo_extra_subscriber(ac, projector) -> None:
    title("7. Thêm subscriber mới (có bộ lọc) mà không sửa publisher")
    critical_only = FilteredAlertSubscriber(
        lambda alert: alert.severity == AlertSeverity.CRITICAL,
        lambda alert: print(f"CRITICAL: {alert.device_id} - {alert.message}"),
    )
    ac.alert_raised += critical_only.handle_alert
    projector.alert_raised += critical_only.handle_alert

    projector.update_battery_level(60)  
    projector.update_battery_level(0)   
  
    ac.update_response_state(True)
    ac.update_response_state(False)

    ac.alert_raised -= critical_only.handle_alert
    projector.alert_raised -= critical_only.handle_alert


def main() -> None:
    projector = ProjectorRemote("PJ-01", "Remote máy chiếu")
    ac = AirConditionerRemote("AC-01", "Remote điều hòa", "A2-301")
    mic = WirelessMicrophone("MIC-01", "Micro không dây")
    devices = [projector, ac, mic]

    notifier = ConsoleNotificationService()
    logger = DeviceAuditLogger()
    maintenance = MaintenanceService()

    coordinator = DeviceMonitoringCoordinator(devices, notifier, logger, maintenance)
    coordinator.subscribe()
    coordinator.subscribe()  
    assert all(len(d.alert_raised) == 2 and len(d.status_changed) == 1 for d in devices)

    try:
        demo_status_changes(projector, mic, logger)
        demo_projector_battery(projector, maintenance)
        demo_air_conditioner(ac, maintenance)
        demo_microphone(mic, maintenance)
        demo_invalid_reading(mic)
        demo_encapsulation(projector)
        demo_extra_subscriber(ac, projector)
    finally:
        coordinator.dispose() 

    title("8. Tổng kết")
    print(f"Audit log: {len(logger.entries)} bản ghi")
    for line in maintenance.requests:
        print(" -", line)

    assert all(len(d.alert_raised) == 0 and len(d.status_changed) == 0 for d in devices)
    count = len(logger.entries)
    projector.change_status(DeviceStatus.AVAILABLE)
    assert len(logger.entries) == count, "sau Dispose logger không được nhận thêm event"

    print("\nTất cả kiểm tra đều đạt.")


if __name__ == "__main__":
    main()