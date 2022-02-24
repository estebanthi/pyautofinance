import unittest

from pyautofinance.tests.test_feed_title import TestFeedTitle
from pyautofinance.tests.test_config import TestConfig
from pyautofinance.tests.test_time_options import TestTimeOptions
from pyautofinance.tests.test_candles_writer import TestWriting
from pyautofinance.tests.test_datafeeds_generators import TestDatafeedsGenerators
from pyautofinance.tests.test_candles_extractor import TestCandlesExtractor
from pyautofinance.tests.test_broker import TestBroker
from pyautofinance.tests.test_strategies import TestStrategies
from pyautofinance.tests.test_engine import TestEngine
from pyautofinance.tests.test_telegram_logger import TestTelegramLogger


def run_some_tests():
    # Run only the tests in the specified classes

    test_classes_to_run = [
        TestConfig,
        TestFeedTitle,
        TestWriting,
        TestCandlesExtractor,
        TestDatafeedsGenerators,
        TestTimeOptions,
        TestBroker,
        TestStrategies,
        TestEngine,
        TestTelegramLogger
    ]

    loader = unittest.TestLoader()

    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    big_suite = unittest.TestSuite(suites_list)

    runner = unittest.TextTestRunner()
    results = runner.run(big_suite)


if __name__ == '__main__':
    run_some_tests()
