class ConfigFileNotFound(BaseException):
    def __init__(self):
        super().__init__(f"config.yml not found")