class ConfigFieldMissing(Exception):
    def __init__(self, field):
        super().__init__(f"Field {field} is missing in config.yml")


class ConfigFileNotFound(BaseException):
    def __init__(self):
        super().__init__(f"config.yml not found")