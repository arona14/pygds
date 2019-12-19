from unittest import TestCase
from pygds.amadeus.xmlbuilders.low_fare_search_helper import generate_number_of_unit, generate_fare_options, generate_pax_reference
from pygds.core.types import TravellerNumbering, TravelFlightInfo, FareOptions


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

    def test_fare_options(self):
        fare = FareOptions()
        result = generate_fare_options(fare)
        self.assertIn("<priceType>RP</priceType>", result)
        self.assertIn("<priceType>RU</priceType>", result)
        self.assertIn("<priceType>ET</priceType>", result)
        self.assertIn("<priceType>TAC</priceType>", result)
        self.assertIn("<priceType>CUC</priceType>", result)
        self.assertIn("<currency>EUR</currency>", result)

    def test_generate_pax_reference(self):
        traveler_number = TravellerNumbering(1, 1)
        result = generate_pax_reference(traveler_number)
        self.assertIn("<ptc>ADT</ptc><traveller><ref>1</ref></traveller>", result)
        self.assertIn("<ptc>CH</ptc><traveller><ref>1</ref></traveller>", result)


class TravelFlightInfoTest(TestCase):

    def test_travel_flight_info(self):
        flight_info = TravelFlightInfo()
        self.assertEqual(flight_info.cabin, "Y")
        self.assertEqual(flight_info.airlines, ["DL", "AF"])
        self.assertEqual(flight_info.rules_cabin, "RC")
        self.assertEqual(flight_info.rules_airline, "F")


if __name__ == "__main__":
    test = LowFareSearchTest()
    test.test_generate_pax_reference()
