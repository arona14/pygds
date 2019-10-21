import unittest
import os
import json
from pygds.env_settings import get_setting
from pygds.core.security_utils import decode_base64


class ClientCan(unittest.TestCase):
    """ This class will test all our function on the client side"""

    def setUp(self) -> None:
        self.pcc = get_setting("SABRE_PCC")
        self.username = get_setting("SABRE_USERNAME")
        self.password = decode_base64(get_setting("SABRE_PASSWORD"))
        base_path = os.path.dirname(os.path.abspath(__file__))
        display_pnr = os.path.join(base_path, "resources/display_pnr.json")
        with open(display_pnr) as j:
            self.display_pnr_json = json.load(j)
        print(self.username, self.password, self.pcc)

    def test_get_reservation(self):
        self.assertIsNotNone(self.display_pnr_json)


if __name__ == "__main__":
    unittest.main()
