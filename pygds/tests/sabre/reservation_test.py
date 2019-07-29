from unittest import TestCase
from pygds.sabre.formatters.reservation_formatter import SabreReservationFormatter


class TestSabreReservation(TestCase):
    """
    This class is use to test all methodes in get reservation
    """
    def setUp(self):
        self.payment_form = ""
        self.itineraire = ""
        self.tickt_info = ""
        self.remark = ""
        self.passenger = ""

    def test_formofpayment(self):
        result = SabreReservationFormatter().formofpayment(self.payment_form)
        self.assertTrue(isinstance(result, object))
        self.assertIsNotNone(result)

    def test_itineraries(self):
        result = SabreReservationFormatter().itineraryInfo(self.itineraire)
        self.assertTrue(isinstance(result, object))
        self.assertIsNotNone(result)

    def test_ticketinginfo(self):
        result = SabreReservationFormatter().ticketing_info(self.tickt_info)
        self.assertTrue(isinstance(result, object))
        self.assertIsNotNone(result)

    def test_passenger(self):
        result = SabreReservationFormatter().get_passengers(self.passenger)
        self.assertTrue(isinstance(result, object))
        self.assertIsNotNone(result)

    def test_remark(self):
        result = SabreReservationFormatter().get_remarks(self.remark)
        self.assertTrue(isinstance(result, object))
        self.assertIsNotNone(result)
