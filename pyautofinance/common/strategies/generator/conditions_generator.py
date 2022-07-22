import random

from pyautofinance.common.strategies.generator.types import Type
from pyautofinance.common.collections.base_collection import BaseCollection
from pyautofinance.common.strategies.generator.condition import Condition
from pyautofinance.common.strategies.generator.lines.value_line import ValueLine


class ConditionsGenerator:

    def generate_operators(self, conditions, possible_operators=['and', 'or']):
        return [random.choice(possible_operators) for i in range(len(conditions)-1)]

    def get_indicators(self, conditions):
        return [indicator for condition in conditions for indicator in condition.get_indicators()]

    def generate_conditions(self, lines_to_use: BaseCollection, n):
        conditions = []
        for i in range(n):
            condition = self.generate_condition(lines_to_use)
            if self._new_condition_is_compatible_with_existing_conditions(condition, conditions):
                conditions.append(condition)
        return conditions

    def _new_condition_is_compatible_with_existing_conditions(self, condition, conditions):
        for existing_condition in conditions:
            if not condition.is_compatible(existing_condition):
                return False
        return True

    def generate_condition(self, lines_to_use: BaseCollection):
        line1 = random.choice(lines_to_use)()
        line1.generate_params()
        continue_loop = True
        while continue_loop:
            line2 = self.generate_compatible_line(lines_to_use, line1)

            line2.generate_params()
            if line1 != line2:
                continue_loop = False


        comparison = self.generate_comparison(line1, line2)
        return Condition(line1, comparison, line2)

    def generate_compatible_line(self, lines_to_use, line):
        if line.type == Type.PRICE_COMPARABLE:
            comparables_lines = lines_to_use.filter(lambda line: line.type == Type.PRICE_COMPARABLE and
                                                                 len(BaseCollection(line.comparisons_available).get_common_items(BaseCollection(line.comparisons_available))) > 0)
            compatible_line = random.choice(comparables_lines)()

        if line.type == Type.RANGE_COMPARABLE:
            compatible_line = ValueLine(possible_values=line.range)

        return compatible_line

    def generate_comparison(self, line1, line2):
        return random.choice(BaseCollection(line1.comparisons_available).get_common_items(BaseCollection(line2.comparisons_available)))

    @staticmethod
    def common_member(a, b):
        a_set = set(a)
        b_set = set(b)
        if len(a_set.intersection(b_set)) > 0:
            return (True)
        return (False)
