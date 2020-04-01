import os
import json
import unittest
import fnc

from pygds.env_settings import get_setting
from pygds.core.security_utils import decode_base64
from pygds.sabre.xmlbuilders.builder import SabreXMLBuilder
from pygds.sabre import helpers
from pygds.sabre.xmlbuilders.sub_parts import get_passengers_in_exchange_shopping, exchange_shopping_passenger, \
    exchange_shopping_segment, get_segments_in_exchange_shopping


class ExchangeShoppingTest(unittest.TestCase):
    """ This class will test all our function on the client side """

    def setUp(self) -> None:
        self.pcc = get_setting("SABRE_PCC")
        self.username = get_setting("SABRE_USERNAME")
        self.password = decode_base64(get_setting("SABRE_PASSWORD"))
        self.rest_url = "https://api.havail.sabre.com"
        self.token = ""
        base_path = os.path.dirname(os.path.abspath(__file__))
        exchange_shopping_request = os.path.join(base_path, "resources/exchangeshopping/exchange_shopping_request.json")
        exchange_shopping_response = os.path.join(base_path, "resources/exchangeshopping/exchange_shopping_response.json")

        with open(exchange_shopping_request) as j:
            self.exchange_shopping_request_json = json.load(j)
        with open(exchange_shopping_response) as r:
            self.exchange_shopping_response_json = json.load(r)

    def test_exchange_shopping_request(self):
        sabre_xml_builder = SabreXMLBuilder(self.rest_url, self.username, self.password, self.pcc)
        request = self.exchange_shopping_request_json
        exchange_shopping = sabre_xml_builder.exchange_shopping_rq(self.token, request["pnr"], request["passengers"], request["segments"])
        self.assertIsNotNone(exchange_shopping)
        exchange_shopping_data = helpers.get_data_from_json(exchange_shopping, "ExchangeShoppingRQ")
        self.assertTrue(isinstance(exchange_shopping_data, dict))
        origin_destination = fnc.get('soapenv:Envelope.soapenv:Body.ExchangeShoppingRQ.OriginDestinationInformation', exchange_shopping_data, default=[])
        self.assertIsNotNone(origin_destination)
        self.assertTrue(isinstance(origin_destination, list))
        passengers_in_exchange_shopping = get_passengers_in_exchange_shopping("ABCDEF", request["passengers"])
        self.assertIsNotNone(passengers_in_exchange_shopping)
        self.assertFalse(isinstance(passengers_in_exchange_shopping, list))
        self.assertTrue(isinstance(passengers_in_exchange_shopping, str))
        first_passenger = request["passengers"][0]

        exchange_passenger = exchange_shopping_passenger("ABCDEF", first_passenger["name_number"], first_passenger["first_name"], first_passenger["last_name"], first_passenger["ticket_number"])
        self.assertIsNotNone(exchange_passenger)
        self.assertFalse(isinstance(exchange_passenger, list))
        self.assertTrue(isinstance(exchange_passenger, str))

        first_segment = request["segments"][0]
        exchange_segment = exchange_shopping_segment(first_segment["departure_date"], first_segment["departure_airport"], first_segment["arrival_airport"])
        self.assertIsNotNone(exchange_segment)
        self.assertFalse(isinstance(exchange_segment, list))
        self.assertTrue(isinstance(exchange_segment, str))

        segments_in_exchange_shopping = get_segments_in_exchange_shopping(request["segments"])
        self.assertIsNotNone(segments_in_exchange_shopping)
        self.assertFalse(isinstance(segments_in_exchange_shopping, list))
        self.assertTrue(isinstance(segments_in_exchange_shopping, str))

    def test_exchange_shopping_response(self):
        self.assertIsNotNone(self.exchange_shopping_response_json)
        self.assertTrue(isinstance(self.exchange_shopping_response_json, dict))


if __name__ == "__main__":
    unittest.main()
