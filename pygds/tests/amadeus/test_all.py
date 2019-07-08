"""
    This is for testing purposes like a suite.
"""

from pygds.amadeus.client import AmadeusClient
from pygds.amadeus.errors import ClientError, ServerError
from pygds.env_settings import get_setting
from pygds.core.types import SellItinerary


def test():
    """ A suite of tests """
    endpoint = get_setting("AMADEUS_ENDPOINT_URL")
    username = get_setting("AMADEUS_USERNAME")
    password = get_setting("AMADEUS_PASSWORD")
    office_id = get_setting("AMADEUS_OFFICE_ID")
    wsap = get_setting("AMADEUS_WSAP")

    client = AmadeusClient(endpoint, username, password, office_id, wsap)
    try:
        # session_info = client.start_new_session()
        # print(session_info)
        search_results = client.fare_master_pricer_travel_board_search("PAR", "WAW", "050819", "100819")
        segments = search_results[0]["segments"][0]
        itineraries = []
        for seg in segments:
            itinerary = SellItinerary(seg["board_airport"], seg["off_airport"], seg["departure_date"], seg["marketing_company"], seg["flight_number"], seg["book_class"], 2)
            itineraries.append(itinerary)
        # print(search_results)
        session = client.sell_from_recommandation(itineraries)
        print(session)
        message_id, session_id, sequence_number, security_token = ("WbsConsu-tuOD826GND68OODM3Qjr0dWw6I2sb6S-EZPmJLtch", session.session_id, session.sequence_number, session.security_token)
        res = client.fare_price_pnr_with_booking_class(message_id, session_id, sequence_number, security_token)
        print(res)
        # tst_reference = res[0]
        # res = client.ticket_create_TST_from_price(message_id, session_id, sequence_number, security_token, tst_reference)
        # print(str(res))
    except ClientError as ce:
        print(f"client_error: {ce}")
    except ServerError as se:
        print(f"server_error: {se}")


if __name__ == "__main__":
    test()
