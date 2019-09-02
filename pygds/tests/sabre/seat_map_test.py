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
        seat_map_xml = client.xml_builder.seap_map_rq("My token", "yes I am here")
        seatmap = client.seat_map("message_id", seat_map_xml)
        print(seatmap)


if __name__ == "__main__":
    unittest.main()
