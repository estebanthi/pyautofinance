class EndDateBeforeStartDate(BaseException):
    def __init__(self):
        super().__init__("End date is before start date")