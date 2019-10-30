"""
    This is for testing purposes like a suite.
"""

from pygds.core.request import RequestedSegment, LowFareSearchRequest
from pygds.core.types import TravellerNumbering, TravellerInfo, ReservationInfo, SellItinerary, Itinerary, FlightSegment
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
        origine, destination, date_dep, date_arr = ("DSS", "CDG", "051119", "071119")

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
             "AF"],
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

        if session_info.session_ended:
            log.error("Session is ended after search")
            return

        message_id = session_info.message_id

        log.info("End of Low Fare Search ********************************************************************************")

        log.info("Begin call of sell from recommandation *************************************************************")

        itineraries = results[0]['itineraries']

        list_segments = []

        itinerary = Itinerary()

        for flight_segment in itineraries:
            segment = flight_segment[0]

            _segment = SellItinerary(
                segment["board_airport"],
                segment["off_airport"],
                segment["departure_date"],
                segment["marketing_company"],
                segment["flight_number"],
                segment["book_class"],
                2
            )
            list_segments.append(_segment)

            itinerary.addSegment(FlightSegment(departure_date_time=segment["departure_date"],
                                               arrival_date_time=segment["arrival_date"],
                                               airline=None,
                                               arrival_airpot=segment["board_airport"],
                                               departure_airport=segment["off_airport"],
                                               flight_number=segment["flight_number"],
                                               marketing=segment["marketing_company"],
                                               class_of_service=segment["book_class"]
                                               ))

        log.info("Begin fare informative pricing without pnr")

        itineraries = [
            itinerary
        ]

        result_informative_pricing = client.fare_informative_price_without_pnr(message_id, TravellerNumbering(2), itineraries)

        log.info(result_informative_pricing)

        log.info("End of informative pricing without pnr")

        result_sell = client.sell_from_recommandation(
            message_id, list_segments
        )

        result_sell, session_info = (result_sell.payload, result_sell.session_info)
        log.info(result_sell)

        if session_info.session_ended:
            log.error("Session is ended after sell from recommendation")
            return
        log.info("End of Sell From Recommandation ******************************************************")
        log.info("Begin Call of Add Passenger Info ****************************************************")

        # message_id = session_info.message_id  # is the message_id to use for the all others actions

<<<<<<< HEAD
        traveller_infos = [TravellerInfo(1, "Amadou", "Diallo", "Diallo", "03121983", "ADT"),
                           TravellerInfo(2, "Khouna", "Khouna", "Fall", "03121976", "ADT")]
=======
        traveller_infos = [TravellerInfo(4, "Mouhamad", "Dianko", "Thiam", "03121990", "ADT"),
                           TravellerInfo(5, "Saliou", "Serigne", "Ndiouck", "03121990", "ADT")]
>>>>>>> 03ae67bb20447cd73e03eec553f9d9cb4c44a07a

        reservation_info = ReservationInfo(traveller_infos, "776656986", "785679876", "saliou@gmail.com")

        passenger_info_response = client.add_passenger_info(office_id, message_id, reservation_info)
        passenger_info_response, session_info = (passenger_info_response.payload, passenger_info_response.session_info)
<<<<<<< HEAD
        log.info(passenger_info_response)

=======
>>>>>>> 03ae67bb20447cd73e03eec553f9d9cb4c44a07a
        if session_info.session_ended:
            log.error("Session is ended after creat pnr")

            return

        # log.info("End of Calling of Add Passenger Information ****************************************")

        # log.info("begin  of Calling of update Passenger Information ****************************************")

        # res_updat_pas = client.pnr_add_multi_for_pax_info_element(message_id, 2, "Diop", 2, "MOUHAMAD", "ADT", 1, "10JUN78")
        # log.debug("update passenger")
        # log.debug(res_updat_pas.payload)

        log.info("Begin SSR DOCS element to the flight segment for ADT Passenger**********************")

        # client.send_command("SR*DOCSYYHK1-----23JUN88-M--DIA-BALLA/P1", message_id)
        # client.send_command("SR*DOCSYYHK1-----23JUN88-M--DIA-BALLA/P2", message_id)

        log.info("End of SSR DOCS element associated to the flight segment for ADT Passenger")

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
        log.info(res_price)

        if session_info.session_ended:

<<<<<<< HEAD
            log.error("Session is ended after price pnr")

            return

        log.info("End of Calling of Price PNR *******************************************************")
=======
        log.info("Begin create pnr")
        pnr = client.create_pnr(message_id)
        log.info(pnr.payload)
        # log.info("Begin SSR DOCS element to the flight segment for ADT Passenger**********************")

        # client.send_command("SR*DOCSYYHK1-----23JUN88-M--DIA-BALLA/P1", message_id)
        # client.send_command("SR*DOCSYYHK1-----23JUN88-M--DIA-BALLA/P2", message_id)

        # log.info("End of SSR DOCS element associated to the flight segment for ADT Passenger")
>>>>>>> 03ae67bb20447cd73e03eec553f9d9cb4c44a07a

        # log.info("Begin Creating TST ********************************************************************")

<<<<<<< HEAD
        tst = res_price[0].fare_reference
        message_id = session_info.message_id
        res_store_price = client.ticket_create_tst_from_price(message_id, tst)
        session_info, res_store_price = (res_store_price.session_info, res_store_price.payload)
        tst_refs = [tst.tst_reference for tst in res_store_price]
        log.info(res_store_price)

        if session_info.session_ended is True:
            log.error("The session is ended when storing TST")
            return
=======
        # tst = res_price[0].fare_reference
        # message_id = session_info.message_id
        # res_store_price = client.ticket_create_tst_from_price(message_id, tst)
        # session_info, res_store_price = (res_store_price.session_info, res_store_price.payload)

        # tst_refs = [tst.tst_reference for tst in res_store_price]
        # if session_info.session_ended is True:
        #     log.error("The session is ended when storing TST")
        #     return
>>>>>>> 03ae67bb20447cd73e03eec553f9d9cb4c44a07a

        # log.info("End of Create TST *****************************************************************")

        # log.info("Begin Add Form of Payment *********************************************************")

<<<<<<< HEAD
        message_id = session_info.message_id
        # fop = CheckPayment("CHEQUE", "MOO")
        # fop = CreditCard(company_id, "VI", "4400009999990004", "999", "", "0838")
        fop = ChashPayment(p_code="CCVI", company_code=company_id)
        res_fop = client.add_form_of_payment(message_id, fop, seg_refs, pax_refs, None, "1")
        log.info(res_fop)

        # if res_fop.session_info.session_ended is True:
=======
        # message_id = session_info.message_id
        # # fop = CheckPayment("CHEQUE", "MOO")
        # fop = CreditCard(company_id, "VI", "4400009999990004", "999", "", "0838")
        # res_fop = client.add_form_of_payment(message_id, fop, seg_refs, pax_refs, None, "1")
        # log.info(type(res_fop))

        # if session_info.session_ended is True:
>>>>>>> 03ae67bb20447cd73e03eec553f9d9cb4c44a07a
        #     log.error("The session is ended when adding Form")
        #     return

        # log.info("End of Add Form of Payment ********************************************************")

<<<<<<< HEAD
        log.info("Begin Save ************************************************************************")
        res_save = client.pnr_add_multi_element(message_id, 11, "AIR")
        session_info, res_save = (res_save.session_info, res_save.payload)
        log.info(res_save)
        pnr = res_save["pnr_header"].controle_number

        if session_info.session_ended is True:
            log.error("The session is ended when saving PNR")
            return
        log.info("End Sqve ****************************************************************************")
=======
        # log.info("Begin Save ************************************************************************")
        # res_save = client.pnr_add_multi_element(message_id, 11, "AIR")
        # session_info, res_save = (res_save.session_info, res_save.payload)
        # log.debug(session_info)
        # log.debug(res_save)
        # if session_info.session_ended is True:
        #     log.error("The session is ended when saving PNR")
        #     return
        # log.info("End Sqve ****************************************************************************")
>>>>>>> 03ae67bb20447cd73e03eec553f9d9cb4c44a07a

        # log.info("Begin Ticket ************************************************************************")

<<<<<<< HEAD
        message_id = session_info.message_id
        res_ticket = client.issue_ticket_with_retrieve(message_id, tst_refs, [])
        session_info, res_ticket = (res_ticket.session_info, res_ticket.payload)
        log.info(res_ticket)

        if session_info.session_ended is True:
            log.error("The session is ended when ticketing")
            return
=======
        # message_id = session_info.message_id
        # res_ticket = client.issue_ticket_with_retrieve(message_id, tst_refs, [])
        # session_info, res_ticket = (res_ticket.session_info, res_ticket.payload)
        # log.info(session_info)
        # log.info(res_ticket)
        # if session_info.session_ended is True:
        #     log.error("The session is ended when ticketing")
        #     return
>>>>>>> 03ae67bb20447cd73e03eec553f9d9cb4c44a07a

        # log.info("End of ticketing **********************************************************************")

<<<<<<< HEAD
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

        client.end_session(message_id)
=======
        # log.info("Begin Place PNR in the Queue ***************************************************************************")
>>>>>>> 03ae67bb20447cd73e03eec553f9d9cb4c44a07a
    except ClientError as ce:
        log.error(f"client_error: {ce}")
        log.error(f"session: {ce.session_info}")
    except ServerError as se:
        log.error(f"server_error: {se}")
        log.error(f"session: {se.session_info}")


if __name__ == "__main__":
    test()
