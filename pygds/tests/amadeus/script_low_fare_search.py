"""
    This is for testing purposes like a suite.
"""

from pygds.core.request import RequestedSegment, LowFareSearchRequest
from pygds.core.types import TravellerNumbering, TravellerInfo, ReservationInfo, SellItinerary
from pygds import log_handler
from pygds.env_settings import get_setting
# from pygds.core.helpers import reformat_date
import os
from pygds.amadeus.client import AmadeusClient
from pygds.amadeus.errors import ClientError, ServerError
from pygds.core.payment import CreditCard
from pygds.core.price import PriceRequest, Fare
# from pygds.core.types import SellItinerary
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
    client = AmadeusClient(endpoint, username, password, office_id, wsap, False)
    try:
        origine, destination, date_dep, date_arr = ("CDG", "DTW", "051119", "071119")
        segments = [RequestedSegment(origin=origine, destination=destination, departure_date=date_dep, arrival_date=date_arr)]
        low_fare_search = LowFareSearchRequest(segments, "Y", "", TravellerNumbering(1), "", "", ["DL", "AF"], "", "", 1)
        log.debug(f"making search from '{origine}' to '{destination}', starting at '{date_dep}' and arriving at '{date_arr}'")
        currency_code, c_qualifier = ("EUR", "RC")
        search_results = client.fare_master_pricer_travel_board_search(low_fare_search, currency_code, c_qualifier)
        log.debug("fare_master_pricer_travel_board_search")
        ressults, session_info = (search_results.payload, search_results.session_info)
        if session_info.session_ended:
            log.error("Session is ended after search")
            return
        log.debug(ressults)
        log.debug("sell_from_recommandation")
        segments = (ressults[0]['itineraries'])
        itineraries = []
        for segment in segments:
            seg = segment[0]
            itinerary = SellItinerary(seg["board_airport"], seg["off_airport"], seg["departure_date"], seg["marketing_company"], seg["flight_number"], seg["book_class"], 2)
            itineraries.append(itinerary)
        choise_segment = client.sell_from_recommandation(itineraries)
        ressults_sell, session_info = (choise_segment.payload, choise_segment.session_info)
        if session_info.session_ended:
            log.error("Session is ended after sell from recommendation")
            return
        log.debug(ressults_sell)
        message_id = session_info.message_id  # is the message_id to use for the all others actions
        traveller_infos = [TravellerInfo(1, "Mouhamad", "Dianko", "Thiam", "03121990", "ADT"),
                           TravellerInfo(2, "Saliou", "Serigne", "Ndiouck", "03121990", "ADT")]
        reservation_info = ReservationInfo(traveller_infos, "776656986", "785679876", "saliou@gmail.com")
        passenger_info_response = client.add_passenger_info(office_id, message_id, reservation_info)
        ressults_add_passengers, session_info = (passenger_info_response.payload, passenger_info_response.session_info)
        if session_info.session_ended:
            log.error("Session is ended after creat pnr")
            return
        log.debug("Result add passengers")
        log.debug(ressults_add_passengers)
        log.debug("Create pnr")
        response_data = client.create_pnr(message_id)

        client.end_session(message_id)
        log.debug(response_data.payload)
        pnr = response_data.payload["pnr_header"].controle_number
        company_id = response_data.payload["pnr_header"].company_id
        log.debug("display pnr " + pnr if pnr is not None else "")
        res_reservation = client.get_reservation(pnr, None, False)
        res_reservation, message_id = res_reservation.payload, res_reservation.session_info.message_id
        log.debug(" result reservation ")
        log.info(res_reservation)
        seg_refs = []
        pax_refs = []
        for seg in res_reservation["itineraries"]:
            seg_refs.append(seg.sequence)
        for pax in res_reservation["passengers"]:
            pax_refs.append(pax.name_id)
        log.info("price pnr")

        print("Add form of payment")
        log.info("4. Add form of payment")
        message_id = session_info.message_id
        # fop = CheckPayment("CHEQUE", "MOO")
        fop = CreditCard(company_id, "VI", "4400009999990004", "999", "", "0838")
        res_fop = client.add_form_of_payment(message_id, fop, seg_refs, pax_refs, None, "1")
        # session_info, res_fop = (res_fop.session_info, res_fop.payload)
        # log.info(session_info)
        log.info(res_fop)
        if session_info.session_ended is True:
            log.error("The session is ended when adding Form")
            return

        log.info("5. Save")
        res_save = client.pnr_add_multi_element(message_id, 11, "AIR")
        session_info, res_save = (res_save.session_info, res_save.payload)
        log.debug(session_info)
        log.debug(res_save)
        if session_info.session_ended is True:
            log.error("The session is ended when saving PNR")
            return

        price_request = PriceRequest(pax_refs, seg_refs)
        log.debug("result of price_request")
        log.debug(price_request)
        res_price = client.fare_price_pnr_with_booking_class(message_id, price_request)
        client.end_session(message_id)
        # mise_a_j = client.send_command("SR*DOCSYYHK1-----23JUN88-M--DIA-BALLA/P1", message_id)
        # mise_a_j = client.send_command("SR*DOCSYYHK1-----23JUN88-M--DIA-BALLA/P2", message_id)
        # r_date = reformat_date("10JUN78", "%d%m%y%H%M", "")

        res_updat_pas = client.pnr_add_multi_for_pax_info_element(message_id, 0, "S1", "Ndiaye", 2, "Ibrahima", "ADT", 1, "10JUN78")
        # log.debug(mise_a_j)
        log.debug("update passenger")
        log.debug(res_updat_pas.payload)
        # client.end_session(message_id)

        log.debug(res_price.payload)
        # log.debug("End ")
        log.debug("End result price")
        chosen_price: Fare = res_price.payload[0]
        log.info(f"Chosen price: {chosen_price}")
        res_tst = client.ticket_create_tst_from_price(message_id, chosen_price.fare_reference)
        log.debug("result TST")
        session_info, res_tst = (res_tst.session_info, res_tst.payload)
        log.debug(res_tst)
        # log.debug("Test queue_place_pnr ")
        # rest_q_place = client.queue_place_pnr(message_id, pnr, [68, 25, 46])
        # log.debug(rest_q_place)

        # log.debug("Test issue_combined")
        # res_issue_combined = client.issue_combined(message_id, pax_refs, seg_refs, False)
        # log.debug(res_issue_combined)
        # log.info(f"session from tst: {session_info}")
        # log.info(f"response from tst: {res_tst}")
        # log.debug(res_tst)
        # rf = client.send_command("RFSaliou", message_id)
        # log.debug(rf)
        # res_issue = client.ticketing_pnr(message_id, "PAX", pax_refs[1])
        # res_issue = client.issue_ticket_with_retrieve(message_id, [1])
        # log.debug(res_issue)
        # res_cancel = client.void_tickets(message_id, [1])
        # log.debug(res_cancel)
    except ClientError as ce:
        log.error(f"client_error: {ce}")
        log.error(f"session: {ce.session_info}")
    except ServerError as se:
        log.error(f"server_error: {se}")
        log.error(f"session: {se.session_info}")


if __name__ == "__main__":
    test()
