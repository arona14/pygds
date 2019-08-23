import unittest
from pygds.core.type_helper import FlightPointDetails, FlightSegment, Itinerary, PassengerPreferences, Passenger, Reservation, TravellerInfo, TravellerNumbering, \
    FormOfPayment, PriceQuote, TicketingInfo


class TypeHelpersTest(unittest.TestCase):
    """ This class will test all our function on the client side """

    def test_fligh_point_details(self):
        result = FlightPointDetails("date", "time", "gmtOffset", "city", "airport",
                                    "gate", "terminal").to_data()
        self.assertIsNotNone(result)

    def test_flight_segment(self):
        result = FlightSegment("sequence", None, None,
                               "airline", "flightNumber", "classOfService", "elapsedTime").to_data()
        self.assertIsNotNone(result)

    def test_itinaries(self):
        r = Itinerary(None)
        result = r.to_data()
        self.assertIsNotNone(result)

    def test_add_segemnt(self):
        r = Itinerary(None)
        iten = r.addSegment(None)
        self.assertIsNotNone(iten)

    def test_price_quote(self):
        f = PriceQuote()
        self.assertIsInstance(f, object)

    def test_form_of_payment(self):
        f = FormOfPayment()
        self.assertIsInstance(f, object)

    def test_ticketing_info(self):
        f = TicketingInfo()
        self.assertIsInstance(f, object)

    def test_pref(self):
        pref = PassengerPreferences({}).to_data()
        self.assertIsNotNone(pref)

    def test_passenger(self):
        passenger = Passenger("Modou", 'Drame', 'M', None,
                              None, None).to_data()
        self.assertIsNotNone(passenger)

    def test_retreive_passaneger(self):
        passenger = Passenger("Modou", 'Drame', 'M', None,
                              None, None)
        self.assertIsNone(passenger.retrievePassengerType())

    def test_reservation(self):
        r = Reservation()
        self.assertIsNotNone(r.to_data())

    def test_add_itineary(self):
        r = Reservation()
        iten = r.addItinerary(None)
        self.assertIsNotNone(iten)

    def test_add_passenger(self):
        r = Reservation()
        passenger = r.addPassenger(None)
        self.assertIsNotNone(passenger)

    def test_travel_info(self):
        t = TravellerInfo(2, "CTS", "Cosmo", "Dakar", "kjjd", "fsff").to_data()
        self.assertIsNone(t)

    def test_travel_numbering_data(self):
        t = TravellerNumbering(2, 0, 1)
        self.assertIsNotNone(t.to_data())
        self.assertEqual(3, t.total_travellers())

    def test_travel_numbering_total(self):
        t = TravellerNumbering(2, 0, 1)
        self.assertEqual(3, t.total_travellers())

    def test_travel_numbering_seat(self):
        t = TravellerNumbering(2, 0, 1)
        self.assertEqual(2, t.total_seats())


if __name__ == "__main__":
    unittest.main()
