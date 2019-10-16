import unittest
from pygds.sabre.client import SabreClient
from pygds.env_settings import get_setting
from pygds.core.security_utils import decode_base64


class ClientCan(unittest.TestCase):
    """ This class will test all our function on the client side"""

    def setUp(self) -> None:
        self.pcc = get_setting("SABRE_PCC")
        self.username = get_setting("SABRE_USERNAME")
        self.password = decode_base64(get_setting("SABRE_PASSWORD"))
        self.rest_url = "https://api.havail.sabre.com"
        self.soap_url = "https://webservices3.sabre.com"
        self.client = SabreClient(self.soap_url, self.rest_url, self.username, self.password, self.pcc, False)
        self.display_pnr = self.client.get_reservation("KZYVQV", None)
        self.session_info = self.display_pnr.session_info
        self.message_id = self.session_info.message_id

        print(self.username, self.password, self.pcc)

    def test_send_command(self):
        result = self.client.send_command(self.message_id, "*KZYVQV")
        self.assertIsNotNone(result, "Cannot sent command")

    def test_get_reservation(self):
        display_pnr = self.client.get_reservation("RBSCCU", None)
        self.assertIsNotNone(display_pnr, "The result of display pnr is None")

    def test_queue_place(self):
        result = self.client.queue_place(self.message_id, 111, "KZYVQV")
        self.assertIsNotNone(result.payload.status)
        self.assertIsNotNone(result.payload.type_response)
        self.assertIsNotNone(result.payload.text_message)
        self.assertEquals(result.payload.status, "Complete")
        self.assertEquals(result.payload.type_response, "Success")

    def test_ignore_transaction(self):
        result = self.client.ignore_transaction(self.message_id)
        self.assertIsNotNone(result.payload.status)
        self.assertIsNotNone(result.payload.create_date_time)
        self.assertTrue(isinstance(result.payload.status, str))
        self.assertTrue(isinstance(result.payload.create_date_time, str))
        self.assertEquals(result.payload.status, "Complete")

    def test_end_transaction(self):
        result = self.client.end_transaction(self.message_id)
        self.assertIsNotNone(result, "Cannot end the transaction")


if __name__ == "__main__":
    unittest.main()
