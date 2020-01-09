"""
    This is for testing purposes like a suite.
"""

from pygds.core.request import RequestedSegment, LowFareSearchRequest
from pygds.core.types import TravellerNumbering, TravellerInfo, ReservationInfo, SellItinerary, FareOptions, TravelFlightInfo
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
        itineraries = [
            RequestedSegment(
                sequence=1, origin="CDG", destination="JFK", departure_date="100120", arrival_date="150120", total_seats=None, airport_city_qualifier="C")]

        traveller = TravellerNumbering(1, 1, 1)

        travel_flight_info = TravelFlightInfo(cabin="Y",
                                              rules_cabin="RC",
                                              airlines=["DL", "AF"],
                                              rules_airline="F")

        fare_options = FareOptions(price_type_et=True,
                                   price_type_rp=True,
                                   price_type_ru=True,
                                   price_type_tac=True,
                                   price_type_cuc=True,
                                   currency_eur=True,
                                   currency_usd=False)

        low_fare_search = LowFareSearchRequest(itineraries, travelingNumber=traveller, fare_options=fare_options, travel_flight_info=travel_flight_info)

        search_results = client.fare_master_pricer_travel_board_search(low_fare_search)
        log.debug("fare_master_pricer_travel_board_search")
        ressults, session_info = (search_results.payload, search_results.session_info)
        log.debug(ressults)
        log.debug("sell_from_recommandation")
        segments = (ressults[0]['itineraries'][0])
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
        create_pnr = client.create_pnr_rq(token, data)
        log.debug(create_pnr)
    except ClientError as ce:
        log.error(f"client_error: {ce}")
        log.error(f"session: {ce.session_info}")
    except ServerError as se:
        log.error(f"server_error: {se}")
        log.error(f"session: {se.session_info}")


if __name__ == "__main__":
    test()
