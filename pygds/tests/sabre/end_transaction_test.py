from unittest import TestCase
from pygds.core.security_utils import decode_base64
from pygds.env_settings import get_setting
from pygds.sabre.client import SabreClient


class TestEndTransaction(TestCase):

    def setUp(self):
        self.username = get_setting("SABRE_USERNAME")
        self.pcc = get_setting("SABRE_PCC")
        self.password = decode_base64(get_setting("SABRE_PASSWORD"))
        self.url = "https://webservices3.sabre.com"
        self.pnr = "DJICXH"
        self.client = SabreClient(self.url, self.username, self.password, self.pcc, False)
        self.token = (self.client.get_reservation(self.pnr, None)).session_info.security_token

    def test_end_transaction(self):
        result = self.client.end_transaction(self.token)
        self.assertIsNotNone(result, "Cannot end the transaction")
