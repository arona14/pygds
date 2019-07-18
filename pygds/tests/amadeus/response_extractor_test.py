from unittest import TestCase

from pygds.amadeus.response_extractor import ErrorExtractor


class ErrorExtractorCan(TestCase):
    def setUp(self) -> None:
        self.xml = ""
        self.extractor = ErrorExtractor(self.xml)

    def init(self):
        extractor = ErrorExtractor(self.xml)
        self.assertIsNotNone(extractor)
        self.assertFalse(extractor.parsed, "The error extractor is parsed on init")

    def parse(self):
        self.extractor.parse()
        self.assertTrue(self.extractor.parsed, "The error extractor is not pared after calling .parse method")

    def extract(self):
        extracted = self.extractor.extract()
        self.assertIsNotNone(extracted, "The extracted error is none")
        self.assertIsNotNone(extracted.session_info)
