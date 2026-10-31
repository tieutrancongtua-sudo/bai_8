class InvalidDeviceReadingException(Exception):

    def __init__(self, device_id: str, invalid_value: int, what: str = "giá trị") -> None:
        super().__init__(f"Thiết bị {device_id}: {what} {invalid_value} nằm ngoài khoảng 0-100")
        self.device_id = device_id
        self.invalid_value = invalid_value
