import os
import json
import unittest
from pygds.sabre.client import SabreClient
from pygds.env_settings import get_setting
from pygds.core.security_utils import decode_base64
from pygds.core.request import RequestedSegment, LowFareSearchRequest, TravellerNumbering


class ClientCan(unittest.TestCase):
    """ This class will test all our function on the client side """

    def setUp(self) -> None:
        self.pcc = get_setting("SABRE_PCC")
        self.username = get_setting("SABRE_USERNAME")
        self.password = decode_base64(get_setting("SABRE_PASSWORD"))
        self.rest_url = "https://api.havail.sabre.com"
        self.client = SabreClient("https://webservices3.sabre.com", self.rest_url, self.username, self.password, self.pcc, False)
        base_path = os.path.dirname(os.path.abspath(__file__))
        json_path_net = os.path.join(base_path, "resources/sfjb/request_builder_net.json")
        json_path_pub = os.path.join(base_path, "resources/sfjb/request_builder_pub.json")
        json_path_response_pub = os.path.join(base_path, "resources/sfjb/response_search_flight.json")

        with open(json_path_pub) as j:
            self.search_pub = json.load(j)

        with open(json_path_net) as k:
            self.search_net = json.load(k)

        with open(json_path_response_pub) as r:
            self.search_response = json.load(r)

    def test_result_search(self):
        segment1 = RequestedSegment("ATH", "LHR", "2019-09-17").to_data()
        segment2 = RequestedSegment("LHR", "ATH", "2019-09-26").to_data()

        segments = []
        segments.append(segment1)
        segments.append(segment2)

        travel_number = TravellerNumbering(1, 0, 0)

        my_request = LowFareSearchRequest(segments, "Y", "WR17", travel_number, [], "50ITINS", [], False, False, 2)
        self.assertNotEqual(my_request, self.search_pub, "They aren't equals")

    def test_travel_numbering(self):
        r = TravellerNumbering(1, 0, 0)
        self.assertIsNotNone(r)

    def test_request_segment(self):
        s = RequestedSegment("DTW", "NYC", "2019-08-29").to_data()
        self.assertEqual(s, {'origin': 'DTW', 'destination': 'NYC', 'departureDate': '2019-08-29'})

    def test_session_token(self):
        session = self.client.session_token()
        self.assertIsNotNone(session, "The result of open session token is None")

    def test_open_session(self):
        session = self.client.open_session()
        self.assertIsNotNone(session, " the result of open session is None")


if __name__ == "__main__":
    unittest.main()
