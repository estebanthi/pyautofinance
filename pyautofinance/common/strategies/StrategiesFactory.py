

class StrategiesFactory:

    @staticmethod
    def make_strategy(strategy, **kwargs):
        return strategy, kwargs
