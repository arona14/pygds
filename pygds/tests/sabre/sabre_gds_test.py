import unittest
from pygds.sabre.sabre_gds import SabreGDS


class ClientCan(unittest.TestCase):
    """ This class will test all our function on the client side """

    def setUp(self) -> None:
        self.pcc = "WR17"
        self.pnr = "oui"
        self.conversation = "okokok"
        self.rest_url = "https://api.havail.sabre.com"

    def test_get_reservation(self):
        result = SabreGDS().get_reservation(self.pnr, self.pcc, self.conversation)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
