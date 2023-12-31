"""
    This is for testing purposes like a suite.
"""

from pygds.core.request import RequestedSegment, LowFareSearchRequest
from pygds.core.types import TravellerNumbering, FareOptions, TravelFlightInfo, SellItinerary, Recommandation, Itinerary, TravellerInfo, Infant, ReservationInfo
from pygds import log_handler
from pygds.env_settings import get_setting
import os
from pygds.amadeus.client import AmadeusClient
from pygds.amadeus.errors import ClientError, ServerError
from pygds.core.price import PriceRequest
from pygds.core.payment import ChashPayment

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
            sequence=1, origin="CDG", destination="DTW", departure_date="291119", arrival_date="081219", total_seats=None, airport_city_qualifier="C")]

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

    low_fare_search = LowFareSearchRequest(
        itineraries, travelingNumber=traveller, fare_options=fare_options, travel_flight_info=travel_flight_info
    )

    search_results = client.fare_master_pricer_travel_board_search(low_fare_search)
    itinerary = search_results.payload[0]["itineraries"][0]

    list_segments = []

    for index, segment in enumerate(itinerary):

        _segment = SellItinerary(
            origin=segment["board_airport"],
            destination=segment["off_airport"],
            departure_date=segment["departure_date"],
            company=segment["marketing_company"],
            flight_number=segment["flight_number"],
            booking_class=segment["book_class"],
            quantity=traveller.total_seats(),
            arrival_date=segment["arrival_date"],
            flight_indicator=index
        )
        list_segments.append(_segment)

    log.info("Begin fare informative pricing without pnr")

    recommandation = Recommandation(list_segments, traveller, FareOptions())

    result_i_b_p_w_p = client.fare_informative_best_pricing_without_pnr(recommandation).payload

    log.info(result_i_b_p_w_p)

    itinerary = Itinerary()
    for segment in list_segments:
        itinerary.addSegment(segment)

    itineraries = [itinerary]
    result_sell_from_rec = client.sell_from_recommandation(itineraries)

    result_sell_from_rec, session_info = result_sell_from_rec.payload, result_sell_from_rec.session_info

    token = session_info.security_token

    inf_am = Infant("Vince", "Faye", "10JAN19")

    inf_k = Infant("Seyni", "Diallo", "10JAN19")

    traveller_infos = [TravellerInfo(
        2, "Amadou", "Diallo", "Diallo", "03121983", "ADT", "P////17MAY12/M/19FEB26/ABRAHAM/SELAH", "amadou@ctsfares.com", "773630684", None
    ),
        TravellerInfo(
        3, "Khouna", "Khouna", "Fall", "03122010", "ADT", "P////17MAY12/F/19FEB26/ABRAHAM/SELAH", "khouna@ctsfares.com", "776689977"
    )]

    reservation_info = ReservationInfo(traveller_infos, number_tel_agent="776656986")

    passenger_info_response = client.add_passenger_info(token, reservation_info)
    passenger_info_response, session_info = (passenger_info_response.payload, passenger_info_response.session_info)
    log.info(passenger_info_response)
    token = session_info.security_token
    seg_refs = []
    pax_refs = []

    for seg in passenger_info_response["itineraries"]:
        seg_refs.append(seg.sequence)

    for pax in passenger_info_response["passengers"]:
        pax_refs.append(pax.name_id)

    price_request = PriceRequest(pax_refs, seg_refs)
    res_price = client.fare_price_pnr_with_booking_class(token, price_request)
    res_price, session_info = res_price.payload, res_price.session_info
    token = session_info.security_token
    log.info(res_price)

    tst_list = [price.fare_reference for price in res_price]
    res_store_price = client.ticket_create_tst_from_price(token, tst_list)
    tst_refs = [tst.tst_reference for tst in res_store_price.payload]
    session_info = res_store_price.session_info
    token = session_info.security_token
    log.info(res_store_price)

    log.info(client.create_tsm(token, pax_refs[0], "F"))
    log.info(client.create_tsm(token, pax_refs[1], "F"))

    fop = ChashPayment(p_code="CCVI", company_code="")
    res_fop = client.add_form_of_payment(token, fop, [], [], None, "1")
    log.info(res_fop)

    res_save = client.pnr_add_multi_element(token, 11, "AIR").payload
    log.info(res_save)
    pnr = res_save["pnr_header"].controle_number
    # res_ticket = client.issue_ticket_with_retrieve(message_id, tst_refs, [])
    res_ticket = client.issue_combined(token, passengers=pax_refs, segments=[], retrieve_pnr=False)
    # session_info, res_ticket = (res_ticket.session_info, res_ticket.payload)
    log.info(res_ticket)

    queue_number = "1"
    queues = list()
    queues.append(queue_number)
    result_queue = client.queue_place_pnr(token, pnr, queues)
    session_info, res_queue = (result_queue.session_info, result_queue.payload)
    log.info(session_info)
    log.info(res_queue)

    client.close_session(token)
except ClientError as ce:
    log.error(f"client_error: {ce}")
    log.error(f"session: {ce.session_info}")
except ServerError as se:
    log.error(f"server_error: {se}")
    log.error(f"session: {se.session_info}")
