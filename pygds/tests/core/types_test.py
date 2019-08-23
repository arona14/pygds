import unittest
from pygds.core.types import FlightPointDetails, FlightSegment, Itinerary, PassengerPreferences, Passenger, Reservation, TravellerInfo, TravellerNumbering, \
    FormOfPayment, PriceQuote, TicketingInfo, FlightAirlineDetails, FlightDisclosureCarrier, FlightMarriageGrp, FlightPriceQuote, FlightAmounts, FlightPassenger_pq, \
    FlightSummary, PnrInfo, Remarks, FareElement, SellItinerary


class TypeHelpersTest(unittest.TestCase):
    """ This class will test all our function on the client side """

    def test_fligh_point_details(self):
        result = FlightPointDetails(None, None, None).to_data()
        self.assertIsNone(result)

    def test_flight_segment(self):
        result = FlightSegment(2, "res_book_desig_code", "departure_date_time",
                               None, None,
                               None, "status", "company_id", "quantity",
                               None, None,
                               "disclosure_carrier", "mariage_group",
                               "seats", "action_code", "segment_special_requests",
                               "schedule_change_indicator", "segment_booked_date", "air_miles_flown",
                               "funnel_flight", "change_of_gauge", "flight_number",
                               "class_of_service", "elapsed_time", "equipment_type",
                               "eticket", "code").to_data()
        self.assertIsNotNone(result)

    def test_itinaries(self):
        r = Itinerary(None, None)
        result = r.to_data()
        self.assertIsNotNone(result)

    def test_add_segemnt(self):
        r = Itinerary(None)
        iten = r.addSegment(None)
        self.assertIsNotNone(iten)

    def test_price_quote(self):
        f = PriceQuote().to_data()
        self.assertIsNotNone(f)

    def test_form_of_payment(self):
        f = FormOfPayment()
        self.assertIsInstance(f, object)

    def test_ticketing_info(self):
        f = TicketingInfo()
        self.assertIsInstance(f, object)

    def test_ticketing_info_data(self):
        f = TicketingInfo().to_data()
        self.assertIsNotNone(f)

    def test_pref(self):
        pref = PassengerPreferences({}).to_data()
        self.assertIsNotNone(pref)

    def test_passenger(self):
        passenger = Passenger("Modou", 'Drame', 'M', None,
                              None, None).to_data()
        self.assertIsNotNone(passenger)

    def test_flight_airline_details(self):
        flight = FlightAirlineDetails("Modou", 'Drame', 'M', None).to_data()
        self.assertIsNotNone(flight)

    def test_flight_disclosure_carrier(self):
        r = FlightDisclosureCarrier(None, None, None)
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

    def test_flight_mariage_gpr(self):
        r = FlightMarriageGrp(None, None, None)
        self.assertIsNotNone(r.to_data())

    def test_flight_pricequote(self):
        flight = FlightPriceQuote("disclosure_carrier", "mariage_group",
                                  "seats", "action_code", "segment_special_requests",
                                  "schedule_change_indicator", "segment_booked_date", "air_miles_flown").to_data()
        self.assertIsNotNone(flight)

    def test_flight_amounts(self):
        flight = FlightAmounts("disclosure_carrier", "mariage_group", "air_miles_flown").to_data()
        self.assertIsNotNone(flight)

    def test_flight_passenger_pq(self):
        flight = FlightPassenger_pq("disclosure_carrier", "mariage_group", "air_miles_flown").to_data()
        self.assertIsNotNone(flight)

    def test_flight_summary(self):
        flight = FlightSummary("disclosure_carrier", "mariage_group", "air_miles_flown").to_data()
        self.assertIsNotNone(flight)

    def test_pnr_info(self):
        pnr = PnrInfo("disclosure_carrier", "mariage_group", "air_miles_flown").to_data()
        self.assertIsNotNone(pnr)

    def test_remarks(self):
        remark = Remarks("disclosure_carrier", "mariage_group", "air_miles_flown").to_data()
        self.assertIsNotNone(remark)

    def test_fare_element(self):
        fare = FareElement("disclosure_carrier", "mariage_group", "air_miles_flown", None, None, None).to_dict()
        self.assertIsNotNone(fare)

    def test_sell_itinaries(self):
        fare = SellItinerary("disclosure_carrier", "mariage_group", "air_miles_flown", None, None, None, None)
        self.assertIsInstance(fare, object)


if __name__ == "__main__":
    unittest.main()
