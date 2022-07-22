import unittest
from unittest.mock import patch, MagicMock, create_autospec

from pyautofinance.common.strategies.generator.conditions_generator import ConditionsGenerator
from pyautofinance.common.strategies.generator.lines.close_line import CloseLine
from pyautofinance.common.strategies.generator.lines.ema_line import EMALine
from pyautofinance.common.collections.base_collection import BaseCollection

class TestConditionsGenerator(unittest.TestCase):

    def test_init(self):
      conditions_generator = ConditionsGenerator()
      self.assertIsNotNone(conditions_generator)

    def test_generate_condition(self):
        lines_to_use = BaseCollection([CloseLine, EMALine])
        conditions_generator = ConditionsGenerator()
        condition = conditions_generator.generate_condition(lines_to_use)
        self.assertIsNotNone(condition)

    def test_generate_conditions(self):
        lines_to_use = BaseCollection([CloseLine, EMALine])
        conditions_generator = ConditionsGenerator()
        conditions = conditions_generator.generate_conditions(lines_to_use, 10)
        print(conditions)

    def test_combine_conditions(self):
        conditions_generator = ConditionsGenerator()
        conditions = conditions_generator.generate_conditions(BaseCollection([CloseLine, EMALine]), 10)
        conditions = conditions_generator.combine_conditions(conditions, ['and', 'or'])
        print(conditions)

    def test_get_indicators(self):
        lines_to_use = BaseCollection([CloseLine, EMALine])
        conditions_generator = ConditionsGenerator()
        conditions = conditions_generator.generate_conditions(lines_to_use, 10)
        indicators = conditions_generator.get_indicators(conditions)
        print(indicators)


if __name__ == '__main__':
    unittest.main()
