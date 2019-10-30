"""
    This is for testing purposes like a suite.
"""

import os
from pygds.amadeus.client import AmadeusClient
from pygds.amadeus.errors import ClientError, ServerError
from pygds.core.payment import CreditCard
from pygds.core.price import PriceRequest
from pygds.env_settings import get_setting
from pygds import log_handler


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
    log = log_handler.get_logger("test_ticket")
    pnr = "LTGPDG"  # "LNB4CC", "LN6C8E", "LMEBKP", "LC87DQ", "LBQ6P9", "L6LMQP", "KDN6HQ", "Q68EFX", "Q68EFX", "RI3B6D", "RT67BC", "RH3WOD", "WKHPRE", "TSYX56", "SNG6IR", "SY9LBS"
    # m_id = None

    client = AmadeusClient(endpoint, username, password, office_id, wsap, True)
    # import web_pdb; web_pdb.set_trace()
    try:
        message_id = None
        log.info("1. Getting Reservation****************************")
        res_reservation = client.get_reservation(pnr, message_id, False)
        session_info, res_reservation = (res_reservation.session_info, res_reservation.payload)
        log.info(session_info)
        log.info(res_reservation)
        if session_info.session_ended is True:
            log.error("The session is ended when retrieving PNR*********************")
            return

        company_id = res_reservation["pnr_header"].company_id
        log.info("2. Pricing PNR ***********************************")
        message_id = session_info.message_id
        passengers = [p.name_id for p in res_reservation["passengers"]]
        print(passengers)
        segments = [s.segment_reference for s in res_reservation["itineraries"]]
        print("****** Values passengers and segments")
        print(passengers, segments)
        price_request = PriceRequest(passengers, segments, "PUB")
        res_price = client.fare_price_pnr_with_booking_class(message_id, price_request)
        session_info, res_price = (res_price.session_info, res_price.payload)
        log.info(session_info)
        log.info(res_price)
        if session_info.session_ended is True:
            log.error("The session is ended when pricing PNR")
            return
        if len(res_price) == 0:
            log.error("No price found")
            return

    log.info("3. Creating TST")
    tst = res_price[0].fare_reference
    message_id = session_info.message_id
    res_store_price = client.ticket_create_tst_from_price(message_id, tst)
    session_info, res_store_price = (res_store_price.session_info, res_store_price.payload)
    log.info(session_info)
    log.info(res_store_price)
    tst_refs = [tst.tst_reference for tst in res_store_price]
    if session_info.session_ended is True:
        log.error("The session is ended when storing TST")
        return

    log.info("4. Add form of payment")
    message_id = session_info.message_id
    # fop = CheckPayment("CHEQUE", "MOO")
    fop = CreditCard(company_id, "VI", "4400009999990004", "999", "", "0838")
    res_fop = client.add_form_of_payment(message_id, fop, segments, passengers, None, "1")
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

    log.info("6. Ticket")
    message_id = session_info.message_id
    res_ticket = client.issue_ticket_with_retrieve(message_id, tst_refs, [])
    session_info, res_ticket = (res_ticket.session_info, res_ticket.payload)
    log.info(session_info)
    log.info(res_ticket)
    if session_info.session_ended is True:
        log.error("The session is ended when ticketing")
        return

        # res_reservation = client.get_reservation(pnr, message_id, False)
        # cancel_response = client.cancel_pnr(message_id, False)
        # session_info, cancel_response = (cancel_response.session_info, cancel_response.payload)
        # log.info(cancel_response)
        # if session_info.session_ended is False:
        #     client.end_session(message_id)
    # elif sesion_info.session_ended is False:
    #     client.end_session(message_id)
    # except ClientError as ce:
    #     log.error(f"client_error: {ce}")
    # log.error(f"session: {ce.session_info}")
    # except ServerError as se:
    #     log.error(f"server_error: {se}")
    #     log.error(f"session: {se.session_info}")


if __name__ == "__main__":
    test()
