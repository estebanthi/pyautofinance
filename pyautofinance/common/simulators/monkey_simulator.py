from pyautofinance.common.results.engine_results_collection import EngineResultsCollection


class MonkeySimulator:

    def __init__(self, monkey_strat, iterations=8000):
        self.iterations = iterations
        self.monkey_strat = monkey_strat

    def simulate(self, engine):

        engine_results = []
        for i in range(self.iterations):
            print(f"Iteration {i}/{self.iterations}")
            engine_result = self._run_once(engine)
            engine_results.append(engine_result)

        return EngineResultsCollection(*engine_results)

    def _run_once(self, engine):
        engine.components_assembly[1] = self.monkey_strat
        return engine.run()
