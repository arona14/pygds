import unittest
import os
import json
import fnc
import xmltodict
from pygds.sabre.xmlbuilders.builder import SabreXMLBuilder


class TicketExchangeableTest(unittest.TestCase):

    def setUp(self):
        base_path = os.path.dirname(os.path.abspath(__file__))
        ticket_exchange_req = os.path.join(base_path, "resources/exchange/exchangeable_request.json")
        with open(ticket_exchange_req) as req:
            self.ticket_request_json = json.load(req)

    def test_builder_ticket_exchangeable(self):
        self.assertIsInstance(self.ticket_request_json, dict)
        token = fnc.get("security_token", self.ticket_request_json)
        ticket_number = self.ticket_request_json['payload']['is_ticket_exchangeable']['ticket_details']['number']
        builder = SabreXMLBuilder("", "", "", "").electronic_document_rq(token=token, ticket_number=ticket_number)
        resp = json.loads(json.dumps(xmltodict.parse(builder)))
        self.assertIsInstance(resp, dict)
        ticket_number_resp_xml = resp['soapenv:Envelope']['soapenv:Body']['GetElectronicDocumentRQ']['SearchParameters']['DocumentNumber']
        token_resp_xml = resp['soapenv:Envelope']['soapenv:Header']['eb:Security']['eb:BinarySecurityToken']
        self.assertIsNotNone(token)
        self.assertEqual(token_resp_xml, token)
        self.assertEqual(ticket_number_resp_xml, ticket_number)


if __name__ == "__main__":
    unittest.main()
