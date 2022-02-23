class EndDateBeforeStartDate(BaseException):
    def __init__(self):
        super().__init__("End date is before start date")


class NoCSVFileFoundWithThoseOptions(BaseException):
    def __init__(self):
        super().__init__("No CSV file with those options has been found")