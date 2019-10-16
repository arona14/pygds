"""
This is for testing purposes like a suite.
"""
from pygds.core.security_utils import decode_base64
from pygds.env_settings import get_setting
from pygds.sabre.client import SabreClient
from pygds.sabre.jsonbuilders.revalidate import Itineraries, FlightSegment


def test():

    username = get_setting("SABRE_USERNAME")
    pcc = get_setting("SABRE_PCC")
    password = decode_base64(get_setting("SABRE_PASSWORD"))
    rest_url = "https://api.havail.sabre.com"
    soap_url = "https://webservices3.sabre.com"
    client = SabreClient(soap_url, rest_url, username, password, pcc, False)
    retrieve_pnr = client.get_reservation("SKENNM", None, True)
    list_itineraries = []
    for itin_index, itin in enumerate(retrieve_pnr.payload["itineraries"]):
        list_segments = []
        for seg in itin.segments:
            flight = FlightSegment()
            flight.flight_number = int(seg.flight_number)
            flight.departure_date_time = seg.departure_date_time
            flight.arrival_date_time = seg.arrival_date_time
            flight.res_book_desig_code = seg.res_book_desig_code
            flight.origin_location = seg.departure_airport.airport
            flight.destination_location = seg.arrival_airpot.airport
            flight.marketing_airline = seg.marketing.airline_code
            flight.operating_airline = seg.operating.airline_code
            list_segments.append(flight.to_dict())
        origin = itin.segments[0].departure_airport.airport
        destination = itin.segments[-1].arrival_airpot.airport
        departure_date = itin.segments[0].departure_date_time
        itinerary = Itineraries(str(itin_index + 1), origin, destination, departure_date, list_segments).to_dict()
        list_itineraries.append(itinerary)
    passengers = [
        {
            "code": "JCB",
            "quantity": 1
        }
    ]
    client.revalidate_itinerary(None, list_itineraries, passengers, "Pub")


if __name__ == "__main__":
    test()
