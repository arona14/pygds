import os
import json
import unittest
from pygds.env_settings import get_setting
from pygds.core.security_utils import decode_base64
from pygds.sabre.xmlbuilders.builder import SabreXMLBuilder
from pygds.sabre import helpers
from pygds.core.payment import CreditCard


class ExchangeCommitTest(unittest.TestCase):
    """ This class will test all our function on the client side """

    def setUp(self) -> None:
        self.pcc = get_setting("SABRE_PCC")
        self.username = get_setting("SABRE_USERNAME")
        self.password = decode_base64(get_setting("SABRE_PASSWORD"))
        self.rest_url = "https://api.havail.sabre.com"
        self.token = ""
        base_path = os.path.dirname(os.path.abspath(__file__))
        exchange_commit_request = os.path.join(base_path, "resources/exchange/exchange_commit_request.json")

        with open(exchange_commit_request) as req:
            self.exchange_commit_request_json = json.load(req)

    def test_exchange_commit_request(self):
        sabre_xml_builder = SabreXMLBuilder(self.rest_url, self.username, self.password, self.pcc)
        request = self.exchange_commit_request_json
        pq = request["price_quote_associated"][0]
        form_of_payment = CreditCard(None, pq["code_card"], pq["number_card"], None, pq["approval_code"], pq["expire_date_card"])
        exchange_commit = sabre_xml_builder.automated_exchanges_commmit_rq(
            self.token,
            pq["price_quote"],
            form_of_payment
        )
        self.assertIsNotNone(exchange_commit)
        exchange_commit_data = helpers.get_data_from_json(exchange_commit, "AutomatedExchangesRQ")
        self.assertTrue(isinstance(exchange_commit_data, dict))


if __name__ == "__main__":
    unittest.main()
