"""
    This is for testing purposes like a suite.
"""

from pygds.core.request import RequestedSegment, LowFareSearchRequest
from pygds.core.types import TravellerNumbering, TravellerInfo, ReservationInfo, SellItinerary
from pygds import log_handler
from pygds.env_settings import get_setting
import os
from pygds.amadeus.client import AmadeusClient
from pygds.amadeus.errors import ClientError, ServerError


def test():
    """ A suite of tests """
    endpoint = get_setting("AMADEUS_ENDPOINT_URL")
    username = get_setting("AMADEUS_USERNAME")
    password = get_setting("AMADEUS_PASSWORD")
    office_id = get_setting("AMADEUS_OFFICE_ID")
    wsap = get_setting("AMADEUS_WSAP")
    dir_path = os.path.dirname(os.path.realpath(__file__))
    dir_path = os.path.join(dir_path, "..", "..", "..")
    os.makedirs(os.path.join(dir_path, "out"), exist_ok=True)
    log_handler.load_file_config(os.path.join(dir_path, "log_config.yml"))
    log = log_handler.get_logger("test_all")
    client = AmadeusClient(endpoint, username, password, office_id, wsap, False)
    try:
        origine, destination, date_dep, date_arr = ("CDG", "DTW", "090120", "150120")
        segments = [RequestedSegment(origin=origine, destination=destination, departure_date=date_dep, arrival_date=date_arr)]
        low_fare_search = LowFareSearchRequest(segments, "Y", "", TravellerNumbering(2), "", "", ["6X"], "", "", 1)
        log.debug(f"making search from '{origine}' to '{destination}', starting at '{date_dep}' and arriving at '{date_arr}'")
        currency_code, c_qualifier = ("EUR", "RC")
        search_results = client.fare_master_pricer_travel_board_search(low_fare_search, currency_code, c_qualifier)
        log.debug("fare_master_pricer_travel_board_search")
        ressults, session_info = (search_results.payload, search_results.session_info)
        log.debug(ressults, session_info)
        log.debug("sell_from_recommandation")
        segments = (ressults[1]['itineraries'])
        print(f" The itineraries : {segments}")
        itineraries = []
        for segment in segments:
            for seg in segment:
                quantities = seg["pax_ref"]
                for quantity in quantities:
                    quant = quantity["traveller"][1]["ref"]
                itinerary = SellItinerary(seg["board_airport"], seg["off_airport"], seg["departure_date"], seg["marketing_company"], seg["flight_number"], seg["book_class"], quant)
                itineraries.append(itinerary)
        token = session_info.security_token  # is the message_id to use for the all others actions
        traveller_infos = [TravellerInfo(1, "Virginie", "Lamesse", "Sy", "03121990", "ADT", ""),
                           TravellerInfo(2, "Ahmadou", "Bamba", "Diagne", "03091992", "ADT", "")]
        reservation_info = ReservationInfo(traveller_infos, "776656986", "785679876", "saliou@gmail.com")
        data = {
            "itineraries": itineraries,
            "passengers": reservation_info
        }
        create_pnr = client._create_pnr(token, data)
        log.debug(create_pnr)
    except ClientError as ce:
        log.error(f"client_error: {ce}")
        log.error(f"session: {ce.session_info}")
    except ServerError as se:
        log.error(f"server_error: {se}")
        log.error(f"session: {se.session_info}")


if __name__ == "__main__":
    test()
