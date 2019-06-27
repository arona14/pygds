from unittest import TestCase
from amadeus.reservation import AmadeusReservation

class TestAmadeusReservation(TestCase):

    def setUp(self):
        self.pnr = ""
        self.pcc = ""
        self.conversation_id = ""
        self.status_session ="InSeries"

    def test_get(self):
        result = AmadeusReservation().get(self.pnr, self.pcc, self.conversation_id, self.status_session)
        self.assertIsNotNone(result)
        self.assertNotEquals(result['itineraries'], [])
        self.assertNotEquals(result['passengers'], [])
        self.assertNotEquals(result['form_of_payments'], [])

