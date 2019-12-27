from pygds.amadeus.xml_parsers.create_tst_extractor import CreateTstResponseExtractor, DisplayTSTExtractor
from pygds.amadeus.xmlbuilders.builder import AmadeusXMLBuilder
from pygds.core.price import TSTInfo
from pygds.core.types import PassengerBasicInfo
from unittest import TestCase


class TestCreateTST(TestCase):
    def setUp(self):
        data_retrieve_pnr_p = open("pygds/tests/amadeus/data/tst.xml")
        data_retrieve_pnr_p = data_retrieve_pnr_p.read()
        self.tst_extractor = CreateTstResponseExtractor(data_retrieve_pnr_p)

    def test_create_tst(self):
        result = self.tst_extractor._extract()
        self.assertEqual(result.pnr, None)
        self.assertEqual(result.status, None)
        self.assertEqual(result.passengers[0].name_id, "2")
        self.assertEqual(result.passengers[0].passenger_type, "PA")

    def tesy_class_tst_info(self):
        tst_infos = TSTInfo(tst_ref="1", passengers=[PassengerBasicInfo(name_id="1", passenger_type="ADT")])
        self.assertEqual(tst_infos.pnr, None)
        self.assertEqual(tst_infos.status, None)
        self.assertEqual(tst_infos.tst_ref, "1")
        self.assertEqual(tst_infos.passengers[0].name_id, "1")
        self.assertEqual(tst_infos.passengers[0].passenger_type, "ADT")


class TestDisplayTST(TestCase):
    def setUp(self):
        data_retrieve_pnr_p = open("pygds/tests/amadeus/data/display_tst.xml")
        data_retrieve_pnr_p = data_retrieve_pnr_p.read()
        self.tst_extractor = DisplayTSTExtractor(data_retrieve_pnr_p)

    def test_display_tst(self):
        extractor = self.tst_extractor._extract()
        self.assertEqual(extractor.status, "ADT")
        self.assertEqual(extractor.air_itinerary_pricing_info[0].tour_code, "")
        self.assertEqual(extractor.air_itinerary_pricing_info[0].valiating_carrier, "6X")
        self.assertEqual(extractor.air_itinerary_pricing_info[0].taxes, "112200.0")
        self.assertEqual(extractor.air_itinerary_pricing_info[0].total_fare, "1324900")


if __name__ == "__main__":
    test = TestCreateTST()
    test.setUp()
    test.test_create_tst()
    test.test_bulder_client()
    test.tesy_class_tst_info()
    test = TestDisplayTST()
    test.setUp()
    test.test_display_tst()
