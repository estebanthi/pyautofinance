class MetricNotFound(BaseException):
    def __init__(self, name):
        super().__init__(f"No metric named {name} in collection")
