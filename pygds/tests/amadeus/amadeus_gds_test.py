from unittest import TestCase

from pygds.amadeus.amadeus_gds import AmadeusGDS


class AmadeusGdsCan(TestCase):
    def setUp(self) -> None:
        self.am = AmadeusGDS()

    def get_reservation(self):
        reservation = self.am.get_reservation("fake-pcc", "fake-pnr", "fake-conv-id")
        self.assertIsNotNone(reservation)

    def search_flights(self):
        res = self.am.search_flights("")
        self.assertIsNone(res, "The result of the method search_flights is not None")

    def create_reservation(self):
        res = self.am.create_reservation("")
        self.assertIsNone(res, "The result of the method create_reservation is not None")

    def price(self):
        res = self.am.price("")
        self.assertIsNone(res, "The result of the method price is not None")

    def ticket(self):
        res = self.am.ticket("")
        self.assertIsNone(res, "The result of the method ticket is not None")

    def void(self):
        res = self.am.void("")
        self.assertIsNone(res, "The result of the method void is not None")

    def cancel(self):
        res = self.am.cancel("")
        self.assertIsNone(res, "The result of the method cancel is not None")

    def exchange_segment(self):
        res = self.am.exchange_segment("")
        self.assertIsNone(res, "The result of the method exchange_segment is not None")

    def refund(self):
        res = self.am.refund("")
        self.assertIsNone(res, "The result of the method refund is not None")

    def rebook_segment(self):
        res = self.am.rebook_segment("")
        self.assertIsNone(res, "The result of the method rebook_segment is not None")

    def update_passenger(self):
        res = self.am.update_passenger("")
        self.assertIsNone(res, "The result of the method update_passenger is not None")
