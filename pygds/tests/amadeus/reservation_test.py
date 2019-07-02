from unittest import TestCase
from pygds.amadeus.reservation import AmadeusReservation

class TestAmadeusReservation(TestCase):

    def setUp(self):
        self.pnr = "RK38GL"
        self.pcc = "DTW1S210B"
        self.conversation_id = "01N2KEFDNH"
        self.status_session ="InSeries"
        self.token = "3OIAKO25LW5TF2GJHQTMJIR891"

    def test_get(self):
        result = AmadeusReservation().get(self.pcc, self.conversation_id, self.status_session)
        self.assertTrue(isinstance(result, object))
        #self.assertIsNotNone(result)
        # self.assertNotEquals(result['itineraries'], [])
        # self.assertNotEquals(result['passengers'], [])
        # self.assertNotEquals(result['form_of_payments'], [])

