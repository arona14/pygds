from unittest import TestCase
from amadeus.helpers import FormatSoapAmadeus

class TestFormatSoapAmadeus(TestCase):

    def setUp(self):
        self.xml_object =""
        self.json_object = soap_service_to_json(self.xml_object)

    def test_soap_service_to_json(self):
        result = FormatSoapAmadeus().soap_service_to_json(self.xml_object)
        self.assertTrue(isinstance(result), str)

    def test_get_segments(self):
        result = FormatSoapAmadeus().get_segments(self.json_object)
        self.assertIsNotNone(result)

    def test_get_passengers(self):
        result = FormatSoapAmadeus().get_passengers(self.json_object)
        self.assertIsNotNone(result)

    def test_get_pnr_infos(self):
        result = FormatSoapAmadeus().get_pnr_infos(self.json_object)
        self.assertIsNotNone(result)

    def test_get_form_of_payments(self):
        result = FormatSoapAmadeus().get_form_of_payments(self.json_object)
        self.assertIsNotNone(result)

    def test_get_price_quotes(self):
        result = FormatSoapAmadeus().get_price_quotes(self.json_object)
        self.assertIsNotNone(result)

    def test_get_ticketing_info(self):
        result = FormatSoapAmadeus().get_ticketing_info(self.json_object)
        self.assertIsNotNone(result)

    def test_get_reservation_response(self):
        result = FormatSoapAmadeus().get_reservation_response(self.json_object)
        self.assertIsNotNone(result)