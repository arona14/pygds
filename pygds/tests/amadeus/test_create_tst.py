from pygds.amadeus.xml_parsers.create_tst_extractor import CreateTstResponseExtractor
from pygds.amadeus.xmlbuilders.builder import AmadeusXMLBuilder
from pygds.core.price import TSTInfo
from pygds.core.types import PassengerBasicInfo
from unittest import TestCase


class TestCreateTST(TestCase):
    def setUp(self):
        data_retrieve_pnr_p = open("pygds/tests/data/tst.xml")
        data_retrieve_pnr_p = data_retrieve_pnr_p.read()
        self.tst_extractor = CreateTstResponseExtractor(data_retrieve_pnr_p)

    def test_create_tst(self):
        result = self.tst_extractor._extract()
        self.assertEqual(result[0].pnr, None)
        self.assertEqual(result[0].status, None)
        self.assertEqual(result[0].passengers[0].name_id, "2")
        self.assertEqual(result[0].passengers[0].passenger_type, "PA")

    def test_bulder_client(self):
        tst_infos = [
            TSTInfo(tst_ref="1", passengers=[PassengerBasicInfo(name_id="1", passenger_type="PA")]),
            TSTInfo(tst_ref="2", passengers=[PassengerBasicInfo(name_id="2", passenger_type="PI")])
        ]
        result = AmadeusXMLBuilder("", "", "", "", "").ticket_create_tst_from_price(None, None, None, None, tst_infos)
        self.assertIn("<referenceDetails><type>PA</type><value>1</value></referenceDetails>", result)
        self.assertIn("<referenceDetails><type>PI</type><value>2</value></referenceDetails>", result)

    def tesy_class_tst_info(self):
        tst_infos = TSTInfo(tst_ref="1", passengers=[PassengerBasicInfo(name_id="1", passenger_type="PA")])
        self.assertEqual(tst_infos.pnr, None)
        self.assertEqual(tst_infos.status, None)
        self.assertEqual(tst_infos.tst_ref, "1")
        self.assertEqual(tst_infos.passengers[0].name_id, "1")
        self.assertEqual(tst_infos.passengers[0].passenger_type, "PA")


if __name__ == "__main__":
    test = TestCreateTST()
    test.setUp()
    test.test_create_tst()
    test.test_bulder_client()
    test.tesy_class_tst_info()
