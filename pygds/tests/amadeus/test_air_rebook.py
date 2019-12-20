from unittest import TestCase

from pygds.amadeus.xmlbuilders.builder import AmadeusXMLBuilder

data = open("pygds/tests/amadeus/data/air_rebook_r.xml")
data = data.read()


class TestRebookAirSegment(TestCase):
    def setUp(self):
        self.extractor = AmadeusXMLBuilder("", "", "", "", "")

    def test_rebook(self):
        result = self.extractor.re_book_air_segment("", "", "", "", [{
            "flight_number": "308498",
            "number_in_party": "2",
            "departure_date_time": "2019-12-31T15:15:00",
            "arrival_date_time": "",
            "origin": "CDG",
            "destination": "DTW",
            "marketing_code": "HK",
            "operating_code": "HK",
            "status": "NN"
        }])
        self.assertIn("<departureDate>191231</departureDate>", result)
        self.assertIn("<departureTime>1515</departureTime>", result)
        self.assertIn("<trueLocationId>CDG</trueLocationId>", result)
        self.assertIn("<trueLocationId>DTW</trueLocationId>", result)
        self.assertIn("<marketingCompany>HK</marketingCompany>", result)
        self.assertIn("<flightNumber>308498</flightNumber>", result)

    def test_rebook_error(self):
        result = self.extractor.re_book_air_segment("", "", "", "", [{
            "flight_number": "308498",
            "number_in_party": "2",
            "departure_date_time": "",
            "arrival_date_time": "",
            "origin": "CDG",
            "destination": "DTW",
            "marketing_code": "HK",
            "operating_code": "HK",
            "status": "NN"
        }])
        self.assertIn("<departureDate>None</departureDate>", result)


if __name__ == "__main__":
    test = TestRebookAirSegment()
    test.setUp()
    test.test_rebook()
    test.test_rebook_error()
