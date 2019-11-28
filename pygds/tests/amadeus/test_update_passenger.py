from unittest import TestCase
from pygds.core.types import FlightPointDetails, FlightAirlineDetails, FlightDisclosureCarrier, FlightMarriageGrp, \
    FlightSegment


class TestAmadeusGds(TestCase):
    """
    This class is to test all function in AmadeusGds
    """
    def test_flight_point_details(self):
        fpd = FlightPointDetails("", "", "").to_data()
        self.assertIsNotNone(fpd)

    def test_flight_air_line_details(self):
        fald = FlightAirlineDetails("", "", "", "").to_data()
        self.assertIsNotNone(fald)

    def test_flight_disclosure_carrier(self):
        fdc = FlightDisclosureCarrier("", "", "").to_data()
        self.assertIsNotNone(fdc)

    def test_flight_marriage_grp(self):
        fm = FlightMarriageGrp("", "", "").to_data()
        self.assertIsNotNone(fm)

    def test_FlightSegment(self):
        flight = FlightSegment(1, "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "").to_data()
        self.assertIsNotNone(flight)
