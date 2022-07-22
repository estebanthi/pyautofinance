from pyautofinance.common.strategies.base_strategy import BaseStrategy
from pyautofinance.common.strategies.generator.condition import Condition


class GeneratedStrategy(BaseStrategy):

    params = (
        ('open_long_conditions', None),
        ('open_long_operators', None),
        ('open_short_conditions', None),
        ('open_short_operators', None),
        ('close_long_conditions', None),
        ('close_long_operators', None),
        ('close_short_conditions', None),
        ('close_short_operators', None),
        ('indicators_storage', None)
    )

    def _init_indicators(self):
        self.indicators = []

        for indicator, params in self.p.indicators_storage.items:
            if not params:
                self.indicators.append(indicator())
            else:
                params = {param.name: param.value for param in params}
                self.indicators.append(indicator(**params))

    def _open_long_condition(self) -> bool:
        return self._evaluate_chain(self.p.open_long_conditions.items, self.p.open_long_operators.items)

    def _open_short_condition(self) -> bool:
        return self._evaluate_chain(self.p.open_short_conditions.items, self.p.open_short_operators.items)

    def _close_long_condition(self) -> bool:
        return self._evaluate_chain(self.p.close_long_conditions.items, self.p.close_long_operators.items)

    def _close_short_condition(self) -> bool:
        return self._evaluate_chain(self.p.close_short_conditions.items, self.p.close_short_operators.items)

    def _get_indicator_value_from_line(self, line):
        for index, indicator in enumerate(self.p.indicators_storage.items):
            if line.parent == indicator[0] and line.params == indicator[1]:
                return self.indicators[index].l.__getattribute__(line.mapping)[0]

    def _check_one_condition(self, condition):
        line1 = condition.line1
        line2 = condition.line2
        comparison = condition.comparison

        value1 = self._get_indicator_value_from_line(line1)
        value2 = self._get_indicator_value_from_line(line2)

        if comparison == '>':
            if value1 > value2:
                return True
        elif comparison == '<':
            if value1 < value2:
                return True
        elif comparison == '>=':
            if value1 >= value2:
                return True
        elif comparison == '<=':
            if value1 <= value2:
                return True
        elif comparison == '==':
            if value1 == value2:
                return True
        elif comparison == '!=':
            if value1 != value2:
                return True
        return False

    def _evaluate_two_conditions(self, condition1, condition2, operator):
        if operator == 'and':
            return self._evaluate_condition(condition1) and self._evaluate_condition(condition2)

        return self._evaluate_condition(condition1) or self._evaluate_condition(condition2)

    def _evaluate_chain(self, conditions, operators):
        if not operators:
            return self._evaluate_condition(conditions[0])

        result = None
        for index, operator in enumerate(operators):
            if result is None:
                result = self._evaluate_two_conditions(conditions[0], conditions[1], operator)
            else:
                result = self._evaluate_two_conditions(result, conditions[index + 1], operator)
        return result

    def _evaluate_condition(self, condition):
        if isinstance(condition, bool):
            return condition
        value1 = self._get_indicator_value_from_line(condition.line1)
        value2 = self._get_indicator_value_from_line(condition.line2)
        comparison = condition.comparison

        if comparison == '>':
            return value1 > value2
        elif comparison == '<':
            return value1 < value2
        elif comparison == '>=':
            return value1 >= value2
        elif comparison == '<=':
            return value1 <= value2
        elif comparison == '==':
            return value1 == value2
        elif comparison == '!=':
            return value1 != value2

        return False

