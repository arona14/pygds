import json
import os

from pygds.sabre.formatters.reservation_formatter import SabreReservationFormatter
# file_path = os.path.dirname(os.getcwd()) + '/pygds/tests/sabre/sabre_get_reservation_response.json'
file_path = os.path.join(os.getcwd(), "pygds", "tests", "sabre", "sabre_get_reservation_response.json")
with open(file_path) as f:

    object_sabre = json.load(f)


def test_price_quote():
    result = object_sabre["or112:PriceQuote"]
    print(result)
    formatter = SabreReservationFormatter()
    pricingquote = formatter.price_quote(result)
    print(pricingquote)


if __name__ == "__main__":
    test_price_quote()

# def test_form_of_payment():
#     result = object_sabre["stl18:Reservation"]["stl18:PassengerReservation"]
#     formatter = SabreReservationFormatter()
#     short_text = formatter.formofpayment(result)
#     print(short_text)


# if __name__ == "__main__":
#     test_form_of_payment()


# def test_segments():
#     segments = object_sabre['stl18:Reservation']['stl18:PassengerReservation']['stl18:Segments']
#     formatter = SabreReservationFormatter()
#     itinerary_info = formatter.itineraryInfo(segments)
#     print(itinerary_info)


# if __name__ == "__main__":
#     test_segments()


# def test_remarks():
#     remark_object = object_sabre["stl18:Reservation"]
#     formatter = SabreReservationFormatter()
#     remark_info = formatter.get_remarks(remark_object)
#     print(remark_info)


# if __name__ == "__main__":
#     test_remarks()

# def test_ticketing_info():
#     result = object_sabre["stl18:Reservation"]["stl18:PassengerReservation"]
#     formatter = SabreReservationFormatter()
#     ticket_infot = formatter.ticketing_info(result)
#     print(ticket_infot)


# if __name__ == "__main__":
#     test_ticketing_info()


# def test_form_of_payment():
#     result = object_sabre["stl18:Reservation"]["stl18:PassengerReservation"]
#     formatter = SabreReservationFormatter()
#     short_text = formatter.formofpayment(result)
#     print(short_text)


# if __name__ == "__main__":
#     test_form_of_payment()


# def test_passenger():
#     passenger_info = SabreReservationFormatter().get_passengers(object_sabre)
#     print(passenger_info)


# if __name__ == "__main__":
#     test_passenger()
