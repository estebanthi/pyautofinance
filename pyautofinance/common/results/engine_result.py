
class EngineResult:

    def __init__(self, engine_result):
        self._engine_result = engine_result

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        if self._index < len(self._engine_result):
            strat_result = self._engine_result[self._index]
            self._index += 1
            return strat_result[0]
        raise StopIteration

    def __contains__(self, item):
        if item in self._engine_result:
            return True
        return False
