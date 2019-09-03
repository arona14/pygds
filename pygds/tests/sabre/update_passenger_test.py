import unittest
from pygds.sabre.client import SabreClient
from pygds.env_settings import get_setting
from pygds.core.security_utils import decode_base64


class UpdatePassengerTest(unittest.TestCase):

    def test_update_passenger(self):
        # write exactly the same test as in previous example
        pcc = get_setting("SABRE_PCC")
        username = get_setting("SABRE_USERNAME")
        password = decode_base64(get_setting("SABRE_PASSWORD"))
        rest_url = "https://api.havail.sabre.com"
        soap_url = "https://webservices3.sabre.com"
        client = SabreClient(soap_url, rest_url, username, password, pcc, False)
        pnr = "XGRJDK"
        air_seat = "My air_seat bloc"
        passenger = "My passenger bloc"
        ssr_code = "My ssr_code bloc"
        dk = "My dk bloc"

        session_info = client.open_session()
        seat_map_xml = client.xml_builder.update_passenger_rq(session_info.security_token, pnr, air_seat, passenger, ssr_code, dk)
        self.assertIsNotNone(seat_map_xml)
        self.assertIn("soapenv:Envelope", seat_map_xml)
        self.assertIn("XGRJDK", seat_map_xml)
        self.assertIn("<Source ReceivedFrom=\"WEBSERVICES\"></Source>", seat_map_xml)
        self.assertIn("<UniqueID id=\"XGRJDK\"/>", seat_map_xml)
        self.assertIn("My air_seat bloc", seat_map_xml)
        self.assertIn("My ssr_code bloc", seat_map_xml)
        self.assertIn("My dk bloc", seat_map_xml)


if __name__ == "__main__":
    unittest.main()
