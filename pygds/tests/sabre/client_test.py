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
        print(self.username, self.password, self.pcc)

    def test_open_session(self):
        session = self.client.open_session()
        self.assertIsNotNone(session, " the result of open session is None")
    
    """
    def test_session_token(self):
        session = self.client.session_token()
        self.assertIsNotNone(session, "The result of open session token is None")
    

    def test_search_flight(self):

        self.assertIsNotNone(search)
    """

if __name__ == "__main__":
    unittest.main()
