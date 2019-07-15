"""
    This is for testing purposes like a suite.
"""

import os

from pygds.amadeus.client import AmadeusClient
from pygds.amadeus.errors import ClientError, ServerError
from pygds.env_settings import get_setting
from pygds.core.types import SellItinerary, TravellerInfo, TravellerNumbering
from pygds import log_handler


def test():
    """ A suite of tests """
    endpoint = get_setting("AMADEUS_ENDPOINT_URL")
    username = get_setting("AMADEUS_USERNAME")
    password = get_setting("AMADEUS_PASSWORD")
    office_id = get_setting("AMADEUS_OFFICE_ID")
    wsap = get_setting("AMADEUS_WSAP")
    file_path = os.path.join(os.getcwd(), "log_config.yml")

    log_handler.load_file_config(file_path)
    log = log_handler.get_logger('test-amadeus')
    log.debug(f"endpoint: {endpoint}, username: {username}, password: ******, office_id: {office_id}, wsap: {wsap}")

    client = AmadeusClient(endpoint, username, password, office_id, wsap)
    try:
        # session_info = client.start_new_session()
        # print(session_info)
        origin, destination, date_dep, date_arr = ("LON", "TYO", "050819", "100819")
        log.debug(f"making search from '{origin}' to '{destination}', starting at '{date_dep}' and arriving at '{date_arr}'")
        search_results = client.fare_master_pricer_travel_board_search(origin, destination, date_dep, date_arr, TravellerNumbering(2))
        log.debug(search_results)
        segments = search_results[0]["itineraries"]
        log.debug(f"segment length: {len(segments)}")
        itineraries = []
        for s in segments:
            seg = s[0]
            itinerary = SellItinerary(seg["board_airport"], seg["off_airport"], seg["departure_date"], seg["marketing_company"], seg["flight_number"], seg["book_class"], 2)
            itineraries.append(itinerary)
        session = client.sell_from_recommandation(itineraries)
        log.debug(session)
        message_id, session_id, sequence_number, security_token = (session.message_id, session.session_id, session.sequence_number + 2, session.security_token)

        pax_infos = [TravellerInfo(1, "Mouhamad", "JJ", "FALL", "03FEV90", "ADT"), TravellerInfo(2, "Maty", "Tima", "SENE", "11NOV95", "ADT")]
        passenger_info_response = client.add_passenger_info(office_id, message_id, session_id, sequence_number, security_token, pax_infos)
        log.debug(passenger_info_response)
        # message_id, session_id, sequence_number, security_token = ("WbsConsu-yOWQzWaBYFcDH2VxGSYmagzKXWMAUE6-VizMC7bnc", "004WZEU0OR", 3, "1QFOF9QSSL6G2ARMEUMY8VYIO")
        price_result = client.fare_price_pnr_with_booking_class(message_id, session_id, sequence_number, security_token)
        log.debug(price_result)
        # tst_reference = res[0]
        # res = client.ticket_create_TST_from_price(message_id, session_id, sequence_number, security_token, tst_reference)
        # print(str(res))
    except ClientError as ce:
        log.error(f"client_error: {ce}")
    except ServerError as se:
        log.error(f"server_error: {se}")


if __name__ == "__main__":
    test()
