from unittest import TestCase
from pygds.amadeus.xmlbuilders.low_fare_search_helper import generate_number_of_unit
from pygds.core.types import TravellerNumbering, TravelFlightInfo


class LowFareSearchTest(TestCase):

    def test_generate_number_of_unit(self):
        traveler = TravellerNumbering(1)

        result = f"""<numberOfUnit>
                <unitNumberDetail>
                    <numberOfUnits>1</numberOfUnits>
                    <typeOfUnit>PX</typeOfUnit>
                </unitNumberDetail>
                <unitNumberDetail>
                    <numberOfUnits>10</numberOfUnits>
                    <typeOfUnit>RC</typeOfUnit>
                </unitNumberDetail>
            </numberOfUnit>
        """
        content = generate_number_of_unit(traveler, "10")

        self.assertEqual(content, result)


class TravelFlightInfoTest(TestCase):

    def test_travel_flight_info(self):
        flight_info = TravelFlightInfo()
        self.assertEqual(flight_info.cabin, "Y")
        self.assertEqual(flight_info.airlines, ["DL", "AF"])
        self.assertEqual(flight_info.rules_cabin, "RC")
        self.assertEqual(flight_info.rules_airline, "F")
