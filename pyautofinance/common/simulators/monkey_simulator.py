from pyautofinance.common.results.engine_results_collection import EngineResultsCollection


class MonkeySimulator:

    def __init__(self, iterations=8000, monkey_full=None, monkey_entry=None, monkey_exit=None):
        self.iterations = iterations
        self.monkey_full = monkey_full
        self.monkey_entry = monkey_entry
        self.monkey_exit = monkey_exit

    def simulate(self, engine):

        results = {'full': [], 'entry': [], 'exit': []}
        for i in range(self.iterations):
            print(f"Iteration {i}/{self.iterations}")

            result = self._run_once(engine)

            for k, v in results.items():
                if k in result:
                    v.append(result[k])

        for k, v in results.items():
            results[k] = EngineResultsCollection(*v) if v else None

        return results

    def _run_once(self, engine):
        results = {}

        if self.monkey_full:
            full_result = self._run_monkey_full(engine)
            results['full'] = full_result

        if self.monkey_entry:
            entry_result = self._run_monkey_entry(engine)
            results['entry'] = entry_result

        if self.monkey_exit:
            exit_result = self._run_monkey_exit(engine)
            results['exit'] = exit_result

        return results

    def _run_monkey_full(self, engine):
        engine.components_assembly[1] = self.monkey_full
        return engine.run()

    def _run_monkey_entry(self, engine):
        engine.components_assembly[1] = self.monkey_entry
        return engine.run()

    def _run_monkey_exit(self, engine):
        engine.components_assembly[1] = self.monkey_exit
        return engine.run()
