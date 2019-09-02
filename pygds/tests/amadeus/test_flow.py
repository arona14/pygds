"""
    This is for testing purposes like a suite.
"""

import os
from pygds.amadeus.client import AmadeusClient
from pygds.amadeus.errors import ClientError, ServerError
from pygds.core.payment import FormOfPayment, CreditCard
from pygds.core.price import PriceRequest, Fare
from pygds.core.types import SellItinerary, TravellerNumbering, TravellerInfo
from pygds.env_settings import get_setting
from pygds import log_handler
# from pygds.core.types import SellItinerary, TravellerInfo, TravellerNumbering


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
    pnr = "JN3IJF"  # "Q68EFX"  # "Q68EFX", "RI3B6D", "RT67BC", "RH3WOD", "WKHPRE", "TSYX56", "SNG6IR", "SY9LBS"
    # m_id = None

    client = AmadeusClient(endpoint, username, password, office_id, wsap, False)
    # import web_pdb; web_pdb.set_trace()
    try:
        res_reservation = client.get_reservation(pnr, None, False)
        # session_info, res_reservation = (res_reservation.session_info, res_reservation.payload)
        # log.info(session_info)
        # log.info(res_reservation)
        # m_id = session_info.message_id
        # seg_refs = []
        # pax_refs = []
        # for seg in res_reservation["itineraries"]:
        #     seg_refs.append(seg.segment_reference)
        # for pax in res_reservation["passengers"]:
        #     pax_refs.append(pax.pax_reference)
        # price_request = PriceRequest(pax_refs, seg_refs)

        # res_price = client.fare_price_pnr_with_booking_class(m_id, price_request)
        # session_info, res_price, app_error = (res_price.session_info, res_price.payload, res_price.application_error)
        # log.debug(session_info)
        # if app_error:
        #     log.error(f"We have an error: {app_error}")
        #     return
        # if len(res_price) <= 0:
        #     log.error("No price proposed")
        #     return
        # # log.info(res_price)
        # chosen_price: Fare = res_price[0]
        # log.info(f"Chosen price: {chosen_price}")
        # m_id = session_info.message_id
        # res_tst = client.ticket_create_tst_from_price(m_id, chosen_price.fare_reference)
        # session_info, res_tst, app_error = (res_tst.session_info, res_tst.payload, res_tst.application_error)
        # log.info(f"session from tst: {session_info}")
        # log.info(f"response from tst: {res_tst}")
        # if app_error:
        #     log.error(f"Something went wrong on create TST: {app_error}")
        #     return
        # _ = client.create_pnr(m_id)

        # logout
        # res_end = client.end_session(session_info.message_id)
        # print(res_end)
        # res_reservation = client.get_reservation(pnr, None, False)
        # session_info, res_reservation = (res_reservation.session_info, res_reservation.payload)
        # res_issue = client.ticketing_pnr(session_info.message_id, "PAX", pax_refs[1])  # i'm changing this
        # res_issue = client.issue_ticket_with_retrieve(session_info.message_id)
        # log.debug(res_issue)  # i'm changing this
        # res_command = client.send_command("IR", m_id)
        # session_info, command_response = (res_command.session_info, res_command.payload)
        # log.info(session_info)
        # log.info(command_response)
        #
        # m_id = session_info.message_id
        # res_command = client.send_command("AD23OCTDTWATH/AAF", m_id)
        # session_info, command_response = (res_command.session_info, res_command.payload)
        # log.info(session_info)
        # log.info(command_response)
        #
        # m_id = session_info.message_id
        # client.fare_price_pnr_with_booking_class(m_id)
        # res_command = client.send_command("SS1X4", m_id)
        # session_info, command_response = (res_command.session_info, res_command.payload)
        # log.info(session_info)
        # log.info(command_response)
        origin, destination, date_dep, date_arr = ("LON", "TYO", "051019", "101019")
        log.debug(f"making search from '{origin}' to '{destination}', starting at '{date_dep}' and arriving at '{date_arr}'")
        search_results = client.fare_master_pricer_travel_board_search(origin, destination, date_dep, date_arr, TravellerNumbering(1))
        log.debug("session after fare_master_pricer_travel_board_search")
        log.debug(search_results.session_info)
        segments = search_results.payload[0]["itineraries"]
        # log.debug(f"segment length: {len(segments)}")
        itineraries = []
        for s in segments:
            seg = s[0]
            itinerary = SellItinerary(seg["board_airport"], seg["off_airport"], seg["departure_date"], seg["marketing_company"], seg["flight_number"], seg["book_class"], 2)
            itineraries.append(itinerary)
        session = client.sell_from_recommandation(itineraries).session_info
        log.debug("session after sell_from_recommandation")
        log.debug(session)
        message_id, session_id, sequence_number, security_token = (session.message_id, session.session_id, session.sequence_number + 2, session.security_token)
        #
        pax_infos = [TravellerInfo(1, "Mouhamad", "JJ", "FALL", "03121990", "ADT"), TravellerInfo(2, "Maty", "Tima", "SENE", "11121995", "ADT")]
        passenger_info_response = client.add_passenger_info(office_id, message_id, session_id, sequence_number, security_token, pax_infos)
        log.debug("session after add_passenger_info")
        log.debug(passenger_info_response.session_info)
        log.debug("passenger after add_passenger_info")
        log.debug(passenger_info_response.payload)
        message_id = passenger_info_response.session_info.message_id
        price_request = PriceRequest(None, None)
        # # message_id, session_id, sequence_number, security_token = ("WbsConsu-yOWQzWaBYFcDH2VxGSYmagzKXWMAUE6-VizMC7bnc", "004WZEU0OR", 3, "1QFOF9QSSL6G2ARMEUMY8VYIO")
        price_result = client.fare_price_pnr_with_booking_class(office_id, message_id, session_id, sequence_number, security_token, pax_infos, price_request)
        log.debug("session after fare_price_pnr_with_booking_class")
        log.debug(price_result)
    except ClientError as ce:
        log.error(f"client_error: {ce}")
        log.error(f"session: {ce.session_info}")
    except ServerError as se:
        log.error(f"server_error: {se}")
        log.error(f"session: {se.session_info}")


if __name__ == "__main__":
    test()
