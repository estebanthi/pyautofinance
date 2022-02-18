import unittest
from feeds.writers.CSVCandlesWriter import CSVCandlesWriter
from feeds.extractors.CSVCandlesExtractor import CSVCandlesExtractor


class TestTimeOptions(unittest.TestCase):

    writer = CSVCandlesWriter()
    extractor = CSVCandlesExtractor


    def test_writing(self):
        pass



if __name__ == '__main__':
    unittest.main()
