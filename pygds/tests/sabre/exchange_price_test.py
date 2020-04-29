import os
import json
import unittest
from pygds.env_settings import get_setting
from pygds.core.security_utils import decode_base64
from pygds.sabre.xmlbuilders.builder import SabreXMLBuilder
from pygds.sabre import helpers
from pygds.core.exchange import PriceDifference, OriginDestination, BaseFare, ItinTotalFare, \
    ExchangeAirItineraryPricingInfo, TaxData, TaxComparison


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
        exchange_price = sabre_xml_builder.automated_exchanges_price_rq(
            self.token,
            request['ticket_number'],
            request['name_number'],
            request['passenger_type'],
            request['markup']
        )
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

    def test_price_difference(self):
        price_difference = PriceDifference("USD", 50)
        self.assertIsNotNone(price_difference)
        self.assertTrue(isinstance(price_difference, PriceDifference))

    def test_origin_destination(self):
        origin_destination = OriginDestination("DSS", "CDG", "100")
        self.assertIsNotNone(origin_destination)
        self.assertTrue(isinstance(origin_destination, OriginDestination))

    def test_pricing_info(self):
        base_fare = BaseFare("100", "USD")
        self.assertIsNotNone(base_fare)
        self.assertTrue(isinstance(base_fare, BaseFare))
        itin_total_fare = ItinTotalFare(base_fare, 500, 670)
        self.assertIsNotNone(itin_total_fare)
        self.assertTrue(isinstance(itin_total_fare, ItinTotalFare))
        pricing_info = ExchangeAirItineraryPricingInfo("O", itin_total_fare)
        self.assertIsInstance(pricing_info, ExchangeAirItineraryPricingInfo)

    def test_tax_comparaison(self):
        list_tax = []
        tax_data_old = TaxData("100", "100")
        tax_data_new = TaxData("50", "50")
        list_tax.append(tax_data_old)
        list_tax.append(tax_data_new)
        tax_comparison = TaxComparison("O")
        tax_comparison.tax = list_tax
        self.assertIsInstance(list_tax, list)
        self.assertIsInstance(tax_data_old, TaxData)
        self.assertIsInstance(tax_data_new, TaxData)
        self.assertIsNotNone(tax_data_old)
        self.assertIsNotNone(tax_data_new)
        self.assertIsNotNone(tax_comparison)
        self.assertIsInstance(tax_comparison, TaxComparison)
        self.assertIsInstance(tax_comparison.to_data(), dict)


if __name__ == "__main__":
    unittest.main()
