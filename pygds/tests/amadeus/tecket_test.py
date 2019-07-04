from unittest import TestCase
from pygds.amadeus.ticket import AmadeusTicketing


class TestAmadeusTicketing(TestCase):

    def setUp(self):
        pass

    def test_add_form_of_payment(self):
        result = AmadeusTicketing().add_form_of_payment()
        pass

    def test_tiketing(self):
        result = AmadeusTicketing().tiketing()
        pass        