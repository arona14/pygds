import unittest
from pygds.sabre.client import SabreClient
from pygds.sabre.session import SabreSession
from pygds.env_settings import get_setting
from pygds.core.security_utils import decode_base64


class ClientCan(unittest.TestCase):
    """ This class will test all our function on the client side """

    def setUp(self) -> None:
        self.pcc = get_setting("SABRE_PCC")
        self.username = get_setting("SABRE_USERNAME")
        self.password = decode_base64(get_setting("SABRE_PASSWORD"))
        self.rest_url = "https://api.havail.sabre.com"
        self.client = SabreClient("https://api.havail.sabre.com", self.rest_url, self.username, self.password, self.pcc, False)
        self.headers = "{'content-type': 'text/xml; charset=utf-8'}"
        print(self.username, self.password, self.pcc)

    def test_open(self):
        result = SabreSession(self.pcc, self.username, self.password, "modou", "https://webservices3.sabre.com", self.headers).open()
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
