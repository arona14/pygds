"""
This is for testing purposes like a suite.
"""
from pygds.sabre.jsonbuilders.revalidate import FlightSegment, Itineraries


def test():

    flight_first_itineratie = []
    flight_second_itineratie = []
    flight_1 = FlightSegment()
    flight_1.flight_number = 3410
    flight_1.departure_date_time = "2019-11-07T14:15:00"
    flight_1.arrival_date_time = "2019-11-07T16:15:00"
    flight_1.res_book_desig_code = "S"
    flight_1.origin_location = "DTW"
    flight_1.destination_location = "EWR"
    flight_1.marketing_airline = "UA"
    flight_1.operating_airline = "UA"

    flight_2 = FlightSegment()
    flight_2.flight_number = 7960
    flight_2.departure_date_time = "2019-11-07T18:25:00"
    flight_2.arrival_date_time = "2019-11-08T07:25:00"
    flight_2.res_book_desig_code = "S"
    flight_2.origin_location = "EWR"
    flight_2.destination_location = "CDG"
    flight_2.marketing_airline = "LH"
    flight_2.operating_airline = "UA"

    flight_first_itineratie.append(flight_1.to_dict())
    flight_first_itineratie.append(flight_2.to_dict())

    flight_3 = FlightSegment()
    flight_3.flight_number = 9334
    flight_3.departure_date_time = "2019-11-28T11:40:00"
    flight_3.arrival_date_time = "2019-11-28T14:10:00"
    flight_3.res_book_desig_code = "S"
    flight_3.origin_location = "CDG"
    flight_3.destination_location = "ORD"
    flight_3.marketing_airline = "LH"
    flight_3.operating_airline = "UA"

    flight_4 = FlightSegment()
    flight_4.flight_number = 5947
    flight_4.departure_date_time = "2019-11-28T15:50:00"
    flight_4.arrival_date_time = "2019-11-28T18:19:00"
    flight_4.res_book_desig_code = "S"
    flight_4.origin_location = "ORD"
    flight_4.destination_location = "DTW"
    flight_4.marketing_airline = "UA"
    flight_4.operating_airline = "UA"

    flight_second_itineratie.append(flight_3.to_dict())
    flight_second_itineratie.append(flight_4.to_dict())
    list_itinerarie = []
    first_itinerary = Itineraries("1", "DTW", "CDG", "2019-11-07T14:15:00", flight_first_itineratie).to_dict()
    second_itinerary = Itineraries("2", "CDG", "DTW", "2019-11-28T11:40:00", flight_second_itineratie).to_dict()
    list_itinerarie.append(first_itinerary)
    list_itinerarie.append(second_itinerary)

    print(list_itinerarie)


if __name__ == "__main__":
    test()
