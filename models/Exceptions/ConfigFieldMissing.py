class ConfigFieldMissing(Exception):

    def __init__(self, field):
        super().__init__(f"Field {field} is missing in config.yml")