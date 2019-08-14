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
        self.client = SabreClient("https://api.havail.sabre.com", self.rest_url, self.username, self.password, self.pcc, False)
        base_path = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(base_path, "resources/sfjb/request_builder.json")
        with open(json_path) as j:
            self.search = json.load(j)

    def test_open_session(self):
        session = self.client.open_session()
        self.assertIsNotNone(session, " the result of open session is None")
        """
        def test_session_token(self):
            session = self.client.session_token()
            self.assertIsNotNone(session, "The result of open session token is None")
        """

    def test_search_flight(self):
        segment1 = RequestedSegment("DTW", "NYC", "2019-08-29").to_data()
        segment2 = RequestedSegment("NYC", "DTW", "2019-09-21").to_data()

        segments = []
        segments.append(segment1)
        segments.append(segment2)

        travel_number = TravellerNumbering(2, 1, 0)

        my_request = LowFareSearchRequest(segments, "Y", "WR17", travel_number, [], "50ITINS", [], False, True, 2)
        my_final_request = self.client.search_flightrq("Modou", my_request, "PUB")
        self.assertEqual(my_final_request, self.search, "The two objets are not equals")

    def test_search


if __name__ == "__main__":
    unittest.main()
