import unittest
from pygds.sabre.client import SabreClient
from pygds.env_settings import get_setting
from pygds.core.security_utils import decode_base64


class SeatMapTest(unittest.TestCase):

    def test_seat_map(self):
        # write exactly the same test as in previous example
        pcc = get_setting("SABRE_PCC")
        username = get_setting("SABRE_USERNAME")
        password = decode_base64(get_setting("SABRE_PASSWORD"))
        rest_url = "https://api.havail.sabre.com"
        soap_url = "https://webservices3.sabre.com"
        client = SabreClient(soap_url, rest_url, username, password, pcc, False)
        session_info = client.open_session()
        seat_map_xml = client.xml_builder.seap_map_rq(session_info.security_token, "Put your flight info here")
        self.assertIsNotNone(seat_map_xml)
        self.assertIn("soapenv:Envelope", seat_map_xml)
        self.assertIn("<tag0:RequestType>Payload</tag0:RequestType>", seat_map_xml)
        self.assertIn("<eb:Service>EnhancedSeatMapRQ</eb:Service>", seat_map_xml)
        self.assertIn("<eb:Action>EnhancedSeatMapRQ</eb:Action>", seat_map_xml)
        self.assertIn("Put your flight info here", seat_map_xml)
