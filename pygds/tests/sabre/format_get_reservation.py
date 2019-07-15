import json
import os

from pygds.sabre.formatters.reservation_formatter import SabreReservationFormatter
# file_path = os.path.dirname(os.getcwd()) + '/pygds/tests/sabre/sabre_get_reservation_response.json'
file_path = os.path.join(os.getcwd(), "pygds", "tests", "sabre", "sabre_get_reservation_response.json")
with open(file_path) as f:

    object_sabre = json.load(f)


def test_segments():
    segments = object_sabre['stl18:Reservation']['stl18:PassengerReservation']['stl18:Segments']
    formatter = SabreReservationFormatter()
    itinerary_info = formatter.itineraryInfo(segments)
    print(itinerary_info)


if __name__ == "__main__":
    test_segments()


# def test_passenger():
#     passenger_info = SabreReservationFormatter().get_passengers(object_sabre)
#     print(passenger_info)


# if __name__ == "__main__":
#     test_passenger()