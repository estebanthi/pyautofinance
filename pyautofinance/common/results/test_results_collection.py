from collections import Counter


class TestResultsCollection:

    def __init__(self, *test_results_list):
        self.test_results = test_results_list

    def __getitem__(self, item):
        return self.test_results[item]

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index < len(self.test_results):
            test_result = self.test_results[self.index]
            self.index += 1
            return test_result

        raise StopIteration

    def validate(self, metrics, validation_functions):
        validations = []
        for result in self.test_results:
            validations.append(result.validate(metrics, validation_functions))
        counter = Counter(validations)
        ok, nok = counter[True], counter[False]
        total = ok + nok
        return {'OK': ok, 'NOK': nok, 'Total': total, 'OK Average': ok/total}
