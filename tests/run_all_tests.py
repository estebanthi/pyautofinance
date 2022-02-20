import unittest
from tests.test_feed_title import TestFeedTitle
from tests.test_config import TestConfig
from tests.test_time_options import TestTimeOptions
from tests.test_candles_writer import TestWriting
from tests.test_datafeeds_generators import TestDatafeedsGenerators
from tests.test_candles_extractor import TestCandlesExtractor


def run_some_tests():
    # Run only the tests in the specified classes

    test_classes_to_run = [
        TestConfig,
        TestFeedTitle,
        TestWriting,
        TestCandlesExtractor,
        TestDatafeedsGenerators,
        TestTimeOptions,
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