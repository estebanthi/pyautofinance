import unittest

from pyautofinance.tests import *


def run_some_tests():
    # Run only the tests in the specified classes

    test_classes_to_run = [
        TestBackDatafeed,
        TestBrokers,
        TestCCXTDatafeed,
        TestConfig,
        TestDataflux,
        TestEngine,
        TestExtractors,
        TestLearn,
        TestMonkeySimulator,
        TestMonkeyStrat,
        TestMonteCarloSimulator,
        TestOHLCV,
        TestPlotting,
        TestResults,
        TestTesters,
        TestTimers,
        TestWalkForwardSimulator,
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
