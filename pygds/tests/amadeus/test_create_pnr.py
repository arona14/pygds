"""
    This is for testing purposes like a suite.
"""

from pygds.core.request import RequestedSegment, LowFareSearchRequest
from pygds.core.types import TravellerNumbering, SellItinerary, FareOptions, TravelFlightInfo
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
                sequence=1, origin="CDG", destination="NCE", departure_date="140120", arrival_date="150120", total_seats=None, airport_city_qualifier="C")]

        traveller = TravellerNumbering(1)

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
        ressults = search_results.payload
        log.debug(ressults)
        log.debug("sell_from_recommandation")
        itinerary = (ressults[0]['itineraries'][0])
        list_segments = []

        passengers = [

            {
                "title": "Mr",
                "given_name": "Elza",
                "surname": "Koepp",
                "middle_name": "",
                "name_number": 1,
                "gender": "Male",
                "date_of_birth": "1990-01-01",
                "passenger_type": "ADT",
                "nationality": "RU",
                "commission_percent": 0,
                "markup": 0,
                "total_fare": 3167.05,
                "currency": "USD",
                "base_fare": 2773,
                "service_fee": 0,
                "ticket_designator": "",
                "tour_code": "",
                "address": "lpkhbcchbjn jd",
                "phone": "965874123",
                "email": "saliou@ctsfares.com",
                "cts_markup": 0,
                "cts_reward": 0,
                "agency_markup": 0,
                "agency_discount": 0
            },
            {
                "title": "Mrs",
                "given_name": "Kelsi",
                "surname": "Hand",
                "middle_name": "",
                "name_number": 2,
                "gender": "Female",
                "date_of_birth": "1990-01-01",
                "passenger_type": "ADT",
                "nationality": "NE",
                "commission_percent": 0,
                "markup": 0,
                "total_fare": 3167.05,
                "currency": "USD",
                "base_fare": 2773,
                "service_fee": 0,
                "ticket_designator": "",
                "tour_code": "",
                "address": "jinjhbvhbhhbh",
                "phone": "",
                "email": "",
                "cts_markup": 0,
                "cts_reward": 0,
                "agency_markup": 0,
                "agency_discount": 0
            },
            {
                "title": "Mr",
                "given_name": "Pearlie",
                "surname": "Kuhlman",
                "middle_name": "",
                "name_number": 3,
                "gender": "Male",
                "date_of_birth": "2009-01-01",
                "passenger_type": "CNN",
                "nationality": "MV",
                "commission_percent": 0,
                "markup": 0,
                "total_fare": 2482.05,
                "currency": "USD",
                "base_fare": 2088,
                "service_fee": 0,
                "ticket_designator": "",
                "tour_code": "",
                "address": "jvjnjnvjfnru",
                "phone": "776919061",
                "email": "",
                "cts_markup": 0,
                "cts_reward": 0,
                "agency_markup": 0,
                "agency_discount": 0
            }
        ]
        for index, segment in enumerate(itinerary):
            _segment = SellItinerary(
                origin=segment["board_airport"],
                destination=segment["off_airport"],
                departure_date=segment["departure_date"],
                company=segment["marketing_company"],
                flight_number=segment["flight_number"],
                booking_class=segment["book_class"],
                quantity=len(passengers),
                arrival_date=segment["arrival_date"],
                flight_indicator=index
            )
            list_segments.append(_segment)

        request = {
            "itineraries": list_segments,
            "passengers": passengers
        }
        create_pnr = client.create_pnr_rq(request)
        log.debug(create_pnr)
    except ClientError as ce:
        log.error(f"client_error: {ce}")
        log.error(f"session: {ce.session_info}")
    except ServerError as se:
        log.error(f"server_error: {se}")
        log.error(f"session: {se.session_info}")


if __name__ == "__main__":
    test()
