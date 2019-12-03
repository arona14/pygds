# """
#     This is for testing purposes like a suite.
# """

import os
from pygds.amadeus.client import AmadeusClient
from pygds.core.payment import ChashPayment
from pygds.core.price import PriceRequest
from pygds.env_settings import get_setting
from pygds import log_handler
import unittest


class PriceTicket(unittest.TestCase):

    def test(self):
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
        pnr = "Q698UG"

        client = AmadeusClient(endpoint, username, password, office_id, wsap, False)
        token = None
        log.info("1. Getting Reservation****************************")
        res_reservation = client.get_reservation(token, False, pnr)
        session_info, res_reservation = (res_reservation.session_info, res_reservation.payload)
        self.assertIsNotNone(res_reservation)
        self.assertIsNotNone(session_info)
        if session_info.session_ended is True:
            log.error("The session is ended when retrieving PNR*********************")
            return

        company_id = res_reservation["pnr_header"].company_id
        self.assertIsNotNone(company_id)
        log.info("2. Pricing PNR ***********************************")
        token = session_info.security_token
        passengers = [p.name_id for p in res_reservation["passengers"]]
        self.assertNotIsInstance(passengers, tuple)
        segments = [s.segment_reference for s in res_reservation["itineraries"]]
        price_request = PriceRequest(passengers, segments, "PUB")
        res_price = client.fare_price_pnr_with_booking_class(token, price_request)
        session_info, res_price = (res_price.session_info, res_price.payload)
        log.info(session_info)
        log.info(" **** Priceinfo ******")
        self.assertNotEqual(res_price, 0)
        self.assertNotIsInstance(res_price, tuple)
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
        self.assertIsNotNone(res_store_price)
        tst_refs = [tst.tst_reference for tst in res_store_price]
        self.assertNotIsInstance(tst_refs, tuple)
        if session_info.session_ended is True:
            log.error("The session is ended when storing TST")
            return

        log.info("4. Add form of payment")
        message_id = session_info.message_id
        fop = ChashPayment(p_code="CCVI", company_code=company_id)

        res_fop = client.add_form_of_payment(message_id, fop, segments, passengers, None, "1")
        self.assertIsNotNone(res_fop)
        log.info(res_fop)
        if session_info.session_ended is True:
            log.error("The session is ended when adding Form")
            return

        log.info("5. Save")
        res_save = client.pnr_add_multi_element(message_id, 11, "AIR")
        session_info, res_save = (res_save.session_info, res_save.payload)
        log.debug(session_info)
        log.debug(res_save)
        self.assertIsNotNone(res_save)
        if session_info.session_ended is True:
            log.error("The session is ended when saving PNR")
            return

        log.info("6. Ticket")
        message_id = session_info.message_id
        res_ticket = client.issue_ticket_with_retrieve(message_id, tst_refs, [])
        session_info, res_ticket = (res_ticket.session_info, res_ticket.payload)
        log.info(session_info)
        self.assertEqual(res_ticket.status, 'O')
        self.assertIsNotNone(res_ticket)
        client.close_session(session_info.message_id)
        if session_info.session_ended is True:
            log.error("The session is ended when ticketing")
            return


if __name__ == "__main__":
    unittest.main()
