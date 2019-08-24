import unittest
from pygds.sabre.client import SabreClient
from pygds.env_settings import get_setting
from pygds.core.security_utils import decode_base64


class ClientCan(unittest.TestCase):
    """ This class will test all our function on the client side """

    def setUp(self) -> None:
        self.pcc = get_setting("SABRE_PCC")
        self.username = get_setting("SABRE_USERNAME")
        self.password = decode_base64(get_setting("SABRE_PASSWORD"))
        self.rest_url = "https://api.havail.sabre.com"
        self.soap_url = "https://webservices3.sabre.com"
        self.client = SabreClient("https://api.havail.sabre.com", self.rest_url, self.username, self.password, self.pcc, False)
        print(self.username, self.password, self.pcc)
    """
    def test_rest_request_wrapper(self):
        session = self.client._rest_request_wrapper(None, None, None)
        print(session)
        self.assertIsInstance(session, object)
    """

    def test_soap_request_wrapper(self):
        session = self.client._soap_request_wrapper("None")
        self.assertIsNotNone(session, "The result of open session token is None")

    """
    def test_get_reservation(self):
        session = self.client.session_token()
        self.assertIsNotNone(session, "The result of open session token is None")
    """


if __name__ == "__main__":
    unittest.main()
