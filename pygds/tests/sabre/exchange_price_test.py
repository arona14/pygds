import os
import json
import unittest
import fnc

from pygds.env_settings import get_setting
from pygds.core.security_utils import decode_base64
from pygds.sabre.xmlbuilders.builder import SabreXMLBuilder
from pygds.sabre import helpers
import fnc

class ExchangePriceTest(unittest.TestCase):
    """ This class will test all our function on the client side """

    def setUp(self) -> None:
        self.pcc = get_setting("SABRE_PCC")
        self.username = get_setting("SABRE_USERNAME")
        self.password = decode_base64(get_setting("SABRE_PASSWORD"))
        self.rest_url = "https://api.havail.sabre.com"
        self.token = ""
        base_path = os.path.dirname(os.path.abspath(__file__))
        exchange_price_request = os.path.join(base_path, "resources/exchangeprice/exchange_price_request.json")

        with open(exchange_price_request) as req:
            self.exchange_shopping_request_json = json.load(req)

    def test_exchange_price_request(self):
        sabre_xml_builder = SabreXMLBuilder(self.rest_url, self.username, self.password, self.pcc)
        request = self.exchange_shopping_request_json
        exchange_price = sabre_xml_builder.automated_exchanges_price_rq(self.token, request['ticket_number'], request['name_number'], request['passenger_type'])
        self.assertIsNotNone(exchange_price)
        exchange_price_data = helpers.get_data_from_json(exchange_price, "ExchangePriceRQ")
        self.assertTrue(isinstance(exchange_price_data, dict))
        exchangeComparison = exchange_price_data['soapenv:Envelope']['soapenv:Body']['AutomatedExchangesRQ']['ExchangeComparison']
        ticket_number_resp = exchangeComparison['@OriginalTicketNumber']
        name_number_resp = exchangeComparison['PriceRequestInformation']['OptionalQualifiers']['PricingQualifiers']['NameSelect']['@NameNumber']
        passenger_type_resp = exchangeComparison['PriceRequestInformation']['OptionalQualifiers']['PricingQualifiers']['PassengerType']['@Code']
        self.assertIsInstance(exchangeComparison, dict)
        self.assertIsNotNone(ticket_number_resp)
        self.assertEqual(ticket_number_resp, request['ticket_number'])
        self.assertEqual(name_number_resp, request['name_number'])
        self.assertEqual(passenger_type_resp, request['passenger_type'])


if __name__ == "__main__":
    unittest.main()


