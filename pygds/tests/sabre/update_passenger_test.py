import unittest
from pygds.sabre.client import SabreClient
from pygds.env_settings import get_setting
from pygds.core.security_utils import decode_base64
from pygds.core.types import PassengerUpdate


class UpdatePassengerTest(unittest.TestCase):

    def test_update_passenger(self):
        # write exactly the same test as in previous example
        pcc = get_setting("SABRE_PCC")
        username = get_setting("SABRE_USERNAME")
        password = decode_base64(get_setting("SABRE_PASSWORD"))
        rest_url = "https://api.havail.sabre.com"
        soap_url = "https://webservices3.sabre.com"
        client = SabreClient(soap_url, rest_url, username, password, pcc, False)
        session_info = client.open_session()
        pnr = "XGRJDK"

        passenger_ssr_code = PassengerUpdate()
        passenger_ssr_code.name_number = "1.1"
        passenger_ssr_code.segment_number = "2"
        passenger_ssr_code.ssr_code = "MLO"
        seat_map_xml = client.xml_builder.update_passenger_rq(session_info.security_token, pnr, passenger_ssr_code)
        self.assertIsNotNone(seat_map_xml)
        self.assertIn("soapenv:Envelope", seat_map_xml)
        self.assertIn("XGRJDK", seat_map_xml)
        self.assertIn("<Service SegmentNumber=\"2\" SSR_Code=\"MLO\">", seat_map_xml)
        self.assertIn("<PersonName NameNumber=\"1.1\"/>", seat_map_xml)

        passenger_dk = PassengerUpdate()
        passenger_dk.dk_number = "DK567826787"
        seat_map_xml = client.xml_builder.update_passenger_rq(session_info.security_token, pnr, passenger_dk)
        self.assertIsNotNone(seat_map_xml)
        self.assertIn("soapenv:Envelope", seat_map_xml)
        self.assertIn("XGRJDK", seat_map_xml)
        self.assertIn("<CustomerIdentifier>DK567826787</CustomerIdentifier>", seat_map_xml)

        passenger_seat = PassengerUpdate()
        passenger_seat.name_number = "1.1"
        passenger_seat.seat_number = "1A"
        passenger_seat.segment_number = "3"
        seat_map_xml = client.xml_builder.update_passenger_rq(session_info.security_token, pnr, passenger_seat)
        self.assertIsNotNone(seat_map_xml)
        self.assertIn("soapenv:Envelope", seat_map_xml)
        self.assertIn("XGRJDK", seat_map_xml)
        self.assertIn("<Seat NameNumber=\"1.1\" Number=\"1A\" SegmentNumber=\"3\"/>", seat_map_xml)

        passenger_info = PassengerUpdate()
        passenger_info.date_of_birth = "10/08/1990"
        passenger_info.gender = "M"
        passenger_info.name_number = "3"
        passenger_info.first_name = "Binete"
        passenger_info.last_name = "Thiam"
        seat_map_xml = client.xml_builder.update_passenger_rq(session_info.security_token, pnr, passenger_info)
        self.assertIsNotNone(seat_map_xml)
        self.assertIn("soapenv:Envelope", seat_map_xml)
        self.assertIn("XGRJDK", seat_map_xml)
        self.assertIn("<PersonName DateOfBirth=\"10/08/1990\" Gender=\"M\" NameNumber=\"3\">", seat_map_xml)
        self.assertIn("<GivenName>Binete</GivenName>", seat_map_xml)
        self.assertIn("<Surname>Thiam</Surname>", seat_map_xml)


if __name__ == "__main__":
    unittest.main()
