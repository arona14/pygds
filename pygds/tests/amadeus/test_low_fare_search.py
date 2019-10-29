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
from pygds.core.payment import CreditCard
from pygds.core.price import PriceRequest

queue_number = "1"


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

    log.info("Begin calling Client API *********************************************")
    client = AmadeusClient(endpoint, username, password, office_id, wsap, False)
    log.info("End of call Client API ***********************************************")

    try:

        log.info("Begin call of Low Fare Search *************************************")
        origine, destination, date_dep, date_arr = ("CDG", "DTW", "051119", "071119")

        segments = [
            RequestedSegment(
                origin=origine,
                destination=destination,
                departure_date=date_dep,
                arrival_date=date_arr)
        ]

        low_fare_search = LowFareSearchRequest(
            segments,
            "Y",
            "",
            TravellerNumbering(1),
            "",
            "",
            ["DL",
             "AF"],
            "",
            "",
            1)

        log.info(f"making search from '{origine}' to '{destination}', starting at '{date_dep}' and arriving at '{date_arr}'")

        currency_code, c_qualifier = ("EUR", "RC")
        search_results = client.fare_master_pricer_travel_board_search(
            low_fare_search, currency_code, c_qualifier
        )

        log.info("End of Low Fare Search ********************************************************************************")

        ressults, session_info = (search_results.payload, search_results.session_info)

        if session_info.session_ended:
            log.error("Session is ended after search")
            return

        log.info("Begin call of sell from recommandation *************************************************************")

        itineraries = ressults[0]['itineraries']

        list_segments = []

        for flight_segment in itineraries:

            segment = flight_segment[0]

            segment = SellItinerary(
                segment["board_airport"],
                segment["off_airport"],
                segment["departure_date"],
                segment["marketing_company"],
                segment["flight_number"],
                segment["book_class"],
                2
            )

            list_segments.append(segment)

        result_sell = client.sell_from_recommandation(
            list_segments
        )

        result_sell, session_info = (result_sell.payload, result_sell.session_info)

        if session_info.session_ended:

            log.error("Session is ended after sell from recommendation")

            return

        log.info("End of Sell From Recommandation ******************************************************")

        log.info("Begin Call of Add Passenger Info ****************************************************")

        message_id = session_info.message_id  # is the message_id to use for the all others actions

        traveller_infos = [TravellerInfo(4, "Mouhamad", "Dianko", "Thiam", "03121990", "ADT"),
                           TravellerInfo(5, "Saliou", "Serigne", "Ndiouck", "03121990", "ADT")]

        reservation_info = ReservationInfo(traveller_infos, "776656986", "785679876", "saliou@gmail.com")

        passenger_info_response = client.add_passenger_info(office_id, message_id, reservation_info)
        passenger_info_response, session_info = (passenger_info_response.payload, passenger_info_response.session_info)
        if session_info.session_ended:

            log.error("Session is ended after creat pnr")

            return

        # log.info("End of Calling of Add Passenger Information ****************************************")

        # log.info("begin  of Calling of update Passenger Information ****************************************")

        # res_updat_pas = client.pnr_add_multi_for_pax_info_element(message_id, 2, "Diop", 2, "MOUHAMAD", "ADT", 1, "10JUN78")
        # log.debug("update passenger")
        # log.debug(res_updat_pas.payload)

        log.info("Begin Call of Pricing Segment for some passenger ***********************************")
        company_id = passenger_info_response["pnr_header"].company_id

        seg_refs = []
        pax_refs = []
        for seg in passenger_info_response["itineraries"]:
            seg_refs.append(seg.sequence)
        for pax in passenger_info_response["passengers"]:
            pax_refs.append(pax.name_id)

        price_request = PriceRequest(pax_refs, seg_refs)
        res_price = client.fare_price_pnr_with_booking_class(message_id, price_request)
        session_info, res_price = (res_price.session_info, res_price.payload)

        log.info("End of Callinf of Price PNR *******************************************************")

        log.info("Begin create pnr")
        pnr = client.create_pnr(message_id)
        log.info(pnr.payload)
        # log.info("Begin SSR DOCS element to the flight segment for ADT Passenger**********************")

        # client.send_command("SR*DOCSYYHK1-----23JUN88-M--DIA-BALLA/P1", message_id)
        # client.send_command("SR*DOCSYYHK1-----23JUN88-M--DIA-BALLA/P2", message_id)

        # log.info("End of SSR DOCS element associated to the flight segment for ADT Passenger")

        # log.info("Begin Creating TST ********************************************************************")

        # tst = res_price[0].fare_reference
        # message_id = session_info.message_id
        # res_store_price = client.ticket_create_tst_from_price(message_id, tst)
        # session_info, res_store_price = (res_store_price.session_info, res_store_price.payload)

        # tst_refs = [tst.tst_reference for tst in res_store_price]
        # if session_info.session_ended is True:
        #     log.error("The session is ended when storing TST")
        #     return

        # log.info("End of Create TST *****************************************************************")

        # log.info("Begin Add Form of Payment *********************************************************")

        # message_id = session_info.message_id
        # # fop = CheckPayment("CHEQUE", "MOO")
        # fop = CreditCard(company_id, "VI", "4400009999990004", "999", "", "0838")
        # res_fop = client.add_form_of_payment(message_id, fop, seg_refs, pax_refs, None, "1")
        # log.info(type(res_fop))

        # if session_info.session_ended is True:
        #     log.error("The session is ended when adding Form")
        #     return

        # log.info("End of Add Form of Payment ********************************************************")

        # log.info("Begin Save ************************************************************************")
        # res_save = client.pnr_add_multi_element(message_id, 11, "AIR")
        # session_info, res_save = (res_save.session_info, res_save.payload)
        # log.debug(session_info)
        # log.debug(res_save)
        # if session_info.session_ended is True:
        #     log.error("The session is ended when saving PNR")
        #     return
        # log.info("End Sqve ****************************************************************************")

        # log.info("Begin Ticket ************************************************************************")

        # message_id = session_info.message_id
        # res_ticket = client.issue_ticket_with_retrieve(message_id, tst_refs, [])
        # session_info, res_ticket = (res_ticket.session_info, res_ticket.payload)
        # log.info(session_info)
        # log.info(res_ticket)
        # if session_info.session_ended is True:
        #     log.error("The session is ended when ticketing")
        #     return

        # log.info("End of ticketing **********************************************************************")

        # log.info("Begin Place PNR in the Queue ***************************************************************************")
    except ClientError as ce:
        log.error(f"client_error: {ce}")
        log.error(f"session: {ce.session_info}")
    except ServerError as se:
        log.error(f"server_error: {se}")
        log.error(f"session: {se.session_info}")


if __name__ == "__main__":
    test()
