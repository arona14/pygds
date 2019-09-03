import unittest
from pygds.sabre.reservation import reformat_sabre_get_reservation, SabreReservation


class ClientCan(unittest.TestCase):
    """ This class will test all our function on the client side """

    def setUp(self) -> None:
        self.pcc = "WR17"
        self.pnr = "oui"
        self.conversation = "okokok"
        self.rest_url = "https://api.havail.sabre.com"

    def test_reformat_sabre_get_reservation(self):
        result = reformat_sabre_get_reservation("test me please")
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        self.assertIn("Itineraries", result)
        self.assertIsInstance(result["Itineraries"], list)
        self.assertIn("Passengers", result)
        self.assertIsInstance(result["Passengers"], list)
        self.assertIn("FormOfPayments", result)
        self.assertIsInstance(result["FormOfPayments"], list)
        self.assertIn("PriceQuotes", result)
        self.assertIsInstance(result["PriceQuotes"], list)
        self.assertIn("TicketingInfo", result)
        self.assertIsInstance(result["TicketingInfo"], list)
        self.assertIn("Remarks", result)
        self.assertIsInstance(result["Remarks"], list)

    def test_reservation(self):
        result = SabreReservation().get(self.pnr, self.pcc, 'factory-test-pygds')
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
