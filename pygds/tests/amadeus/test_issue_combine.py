"""
    This is for testing purposes like a suite.
"""

from pygds.core.request import RequestedSegment, LowFareSearchRequest
from pygds.core.types import TravellerNumbering, TravellerInfo, ReservationInfo, SellItinerary, Recommandation
from pygds import log_handler
from pygds.env_settings import get_setting

import os
from pygds.amadeus.client import AmadeusClient
from pygds.amadeus.errors import ClientError, ServerError
from pygds.core.payment import ChashPayment
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
    client = AmadeusClient(endpoint, username, password, office_id, wsap, True)
    log.info("End of call Client API ***********************************************")

    try:

        log.info("Begin call of Low Fare Search *************************************")
        origine, destination, date_dep, date_arr = ("CDG", "DTW", "121119", "171119")

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
            TravellerNumbering(2),
            "",
            "",
            ["DL",
             "AF", ],
            "",
            "",
            1)

        log.info(f"making search from '{origine}' to '{destination}', starting at '{date_dep}' and arriving at '{date_arr}'")
        currency_code, c_qualifier = ("EUR", "RC")
        search_results = client.fare_master_pricer_travel_board_search(
            low_fare_search, currency_code, c_qualifier
        )
        results, session_info = (search_results.payload, search_results.session_info)
        log.info(results)

        log.info("End of Low Fare Search ********************************************************************************")

        log.info("Begin call of sell from recommandation *************************************************************")

        itineraries = results[0]['itineraries']

        list_segments = []

        for index, flight_segment in enumerate(itineraries):
            segment = flight_segment[0]

            quantities = 0
            for ptc in segment["pax_ref"]:
                quantities += len(ptc["traveller"])

            _segment = SellItinerary(
                origin=segment["board_airport"],
                destination=segment["off_airport"],
                departure_date=segment["departure_date"],
                company=segment["marketing_company"],
                flight_number=segment["flight_number"],
                booking_class=segment["book_class"],
                quantity=quantities,
                arrival_date=segment["arrival_date"],
                flight_indicator=index
            )
            list_segments.append(_segment)

        log.info("Begin fare informative pricing without pnr")

        recommandation = Recommandation(list_segments, TravellerNumbering(2))

        # itineraries = [
        #     itinerary
        # ]

        result_informative_best_pricing = client.fare_informative_best_pricing_without_pnr(recommandation=recommandation)

        log.info(result_informative_best_pricing)

        log.info("End of informative pricing without pnr")

        result_sell = client.sell_from_recommandation(list_segments)

        result_sell, session_info = (result_sell.payload, result_sell.session_info)
        log.info(result_sell)

        message_id = session_info.message_id

        log.info("End of Sell From Recommandation ******************************************************")
        log.info("Begin Call of Add Passenger Info ****************************************************")

        # message_id = session_info.message_id  # is the message_id to use for the all others actions

        traveller_infos = [TravellerInfo(2, "Amadou", "Diallo", "Diallo", "03121983", "ADT", "P////17MAY12/M/19FEB26/ABRAHAM/SELAH"),
                           TravellerInfo(3, "Khouna", "Khouna", "Fall", "03121976", "ADT", "P////17MAY12/M/19FEB26/ABRAHAM/SELAH")]

        reservation_info = ReservationInfo(traveller_infos, "776656986", "785679876", "saliou@gmail.com")

        passenger_info_response = client.add_passenger_info(office_id, message_id, reservation_info, _segment.company)
        passenger_info_response, session_info = (passenger_info_response.payload, passenger_info_response.session_info)
        log.info(passenger_info_response)

        if session_info.session_ended:
            log.error("Session is ended after creat pnr")

            return

        # log.info("End of Calling of Add Passenger Information ****************************************")

        # log.info("begin  of Calling of update Passenger Information ****************************************")

        # res_updat_pas = client.pnr_add_multi_for_pax_info_element(message_id, 2, "Diop", 2, "MOUHAMAD", "ADT", 1, "10JUN78")
        # log.debug("update passenger")
        # log.debug(res_updat_pas.payload)

        company_id = _segment.company

        seg_refs = []
        pax_refs = []
        for seg in passenger_info_response["itineraries"]:
            seg_refs.append(seg.sequence)
        for pax in passenger_info_response["passengers"]:
            pax_refs.append(pax.name_id)

        # log.info("Begin SSR DOCS element to the flight segment for ADT Passenger**********************")

        # response_ssr = client.pnr_add_ssr(message_id, pax_refs, "P////17MAY12/M/19FEB26/ABRAHAM/SELAH", company_id)
        # response_ssr = client.pnr_add_ssr(message_id, pax_refs[1], "////23JUN88/M//DIA/BALLA", company_id)
        # log.info(response_ssr)

        # log.info("End of SSR DOCS element associated to the flight segment for ADT Passenger")

        log.info("Begin Call of Pricing Segment for some passenger ***********************************")

        price_request = PriceRequest(pax_refs, seg_refs)
        res_price = client.fare_price_pnr_with_booking_class(message_id, price_request)
        session_info, res_price = (res_price.session_info, res_price.payload)
        log.info(res_price)

        if session_info.session_ended:

            log.error("Session is ended after price pnr")

            return

        log.info("End of Calling of Price PNR *******************************************************")

        # log.info("Begin Creating TST ********************************************************************")

        tst = res_price[0].fare_reference
        message_id = session_info.message_id
        res_store_price = client.ticket_create_tst_from_price(message_id, tst)
        session_info, res_store_price = (res_store_price.session_info, res_store_price.payload)
        # tst_refs = [tst.tst_reference for tst in res_store_price]
        log.info(res_store_price)

        if session_info.session_ended is True:
            log.error("The session is ended when storing TST")
            return

        # log.info("End of Create TST *****************************************************************")

        # log.info("Begin Add Form of Payment *********************************************************")

        message_id = session_info.message_id
        # fop = CheckPayment("CHEQUE", "MOO")
        # fop = CreditCard(company_id, "VI", "4400009999990004", "999", "", "0838")
        fop = ChashPayment(p_code="CCVI", company_code=company_id)
        res_fop = client.add_form_of_payment(message_id, fop, seg_refs, pax_refs, None, "1")
        log.info(res_fop)

        log.info(client.create_tsm(message_id, pax_refs[0], "f"))
        log.info(client.create_tsm(message_id, pax_refs[1], "f"))
        # if res_fop.session_info.session_ended is True:
        #     log.error("The session is ended when adding Form")
        #     return

        # log.info("End of Add Form of Payment ********************************************************")

        log.info("Begin Save ************************************************************************")
        res_save = client.pnr_add_multi_element(message_id, 11, "AIR")
        session_info, res_save = (res_save.session_info, res_save.payload)
        log.info(res_save)
        pnr = res_save["pnr_header"].controle_number

        if session_info.session_ended is True:
            log.error("The session is ended when saving PNR")
            return
        log.info("End Save ****************************************************************************")

        # log.info("Begin Ticket ************************************************************************")

        message_id = session_info.message_id
        # res_ticket = client.issue_ticket_with_retrieve(message_id, tst_refs, [])
        res_ticket = client.issue_combined(message_id, passengers=pax_refs, segments=[], retrieve_pnr=False)
        # session_info, res_ticket = (res_ticket.session_info, res_ticket.payload)
        log.info(res_ticket)

        if session_info.session_ended is True:
            log.error("The session is ended when ticketing")
            return

        # log.info("End of ticketing **********************************************************************")

        log.info("Begin Placing PNR in the Queue ********************************************************")

        global queue_number
        queues = list()
        queues.append(queue_number)
        result_queue = client.queue_place_pnr(message_id, pnr, queues)
        session_info, res_queue = (result_queue.session_info, result_queue.payload)
        log.info(session_info)
        log.info(res_queue)
        if session_info.session_ended is True:
            log.error("The session is ended when place pnr in the queue")
            return

        client.close_session(message_id)
    except ClientError as ce:
        log.error(f"client_error: {ce}")
        log.error(f"session: {ce.session_info}")
    except ServerError as se:
        log.error(f"server_error: {se}")
        log.error(f"session: {se.session_info}")


if __name__ == "__main__":
    test()
