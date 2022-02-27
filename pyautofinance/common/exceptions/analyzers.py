class AnalyzerMissing(BaseException):
    def __init__(self, analyzer_name):
        super().__init__(f"{analyzer_name} analyzer missing or wrong named")