import unittest
from pygds.sabre.client import SabreClient
from pygds.env_settings import get_setting
from pygds.core.security_utils import decode_base64
from pygds.core.request import RequestedSegment, TravellerNumbering
from pygds.core.sessions import SessionInfo


class ClientCan(unittest.TestCase):
    """ This class will test all our function on the client side """

    def setUp(self) -> None:
        self.pcc = get_setting("SABRE_PCC")
        self.username = get_setting("SABRE_USERNAME")
        self.password = decode_base64(get_setting("SABRE_PASSWORD"))
        self.rest_url = "https://api.havail.sabre.com"
        self.soap_url = "https://webservices3.sabre.com"
        self.client = SabreClient(self.soap_url, self.rest_url, self.username, self.password, self.pcc, False)

    def test_travel_numbering(self):
        r = TravellerNumbering(1, 2, 3)
        self.assertIsNotNone(r)
        self.assertEqual(r.children, 2)
        self.assertEqual(r.infants, 3)
        self.assertEqual(r.adults, 1)

    def test_request_segment(self):
        s = RequestedSegment(1, "DTW", "NYC", "2019-09-24", "2019-09-29", "1").to_data()
        self.assertEqual(s, {'sequence': 1, 'origin': 'DTW', 'destination': 'NYC', 'departure_date': '2019-09-24', "arrival_date": '2019-09-29', 'total_seats': '1'})
        self.assertIsInstance(s, dict)
        self.assertIn('origin', s)
        self.assertEqual('DTW', s["origin"])
        self.assertEqual('NYC', s["destination"])

    def test_session_token(self):
        session = self.client.open_session()
        self.assertIsNotNone(session, "The result of open session token is None")
        self.assertIsNotNone(session.security_token, "You don't got a token")
        self.assertIsInstance(session.session_ended, bool)
        self.assertIsInstance(session, SessionInfo)

    def test_open_session(self):
        session = self.client.open_session()
        self.assertIsNotNone(session, " the result of open session is None")
        self.assertIsInstance(session, SessionInfo)
        self.assertIn("Shared", session.security_token)
