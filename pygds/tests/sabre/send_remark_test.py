import unittest
from pygds.sabre.client import SabreClient
from pygds.env_settings import get_setting
from pygds.core.security_utils import decode_base64
from pygds.amadeus.amadeus_types import GdsResponse
from pygds.core.helpers import get_data_from_json as from_json


class SendRemarkTest(unittest.TestCase):

    def setUp(self) -> None:
        self.pcc = get_setting("SABRE_PCC")
        self.username = get_setting("SABRE_USERNAME")
        self.password = decode_base64(get_setting("SABRE_PASSWORD"))
        self.rest_url = ""
        self.client = SabreClient("https://webservices3.sabre.com", self.rest_url, self.username, self.password, self.pcc, False)

    def test_send_remark(self):
        display_pnr = self.client.get_reservation("KZYVQV", None)
        session_info = display_pnr.session_info
        if not session_info:
            print("No session info")
            return
        message_id = session_info.message_id
        self.assertIsNotNone(message_id)
        remark = self.client.send_remark(message_id, 'MBQ')
        self.assertIsNotNone(remark)
        self.assertIsInstance(remark, GdsResponse)
        self.assertEqual(from_json(remark.payload, "status"), 'Complete')


if __name__ == "__main__":
    unittest.main()
