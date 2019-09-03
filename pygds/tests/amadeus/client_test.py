from unittest import TestCase
import unittest
from pygds.amadeus.client import AmadeusClient
# from pygds.core.app_error import ApplicationError
from pygds.env_settings import get_setting
from pygds.errors.gdserrors import NoSessionError


class ClientCan(TestCase):
    def setUp(self) -> None:
        endpoint = get_setting("AMADEUS_ENDPOINT_URL")
        username = get_setting("AMADEUS_USERNAME")
        password = get_setting("AMADEUS_PASSWORD")
        office_id = get_setting("AMADEUS_OFFICE_ID")
        wsap = get_setting("AMADEUS_WSAP")
        self.client = AmadeusClient(endpoint, username, password, office_id, wsap, False)

    """def test_send_command(self):
        seq, m_id = (None, None)
        pnr = "Q68EFX"
        res_command = self.client.send_command(f"RT{pnr}", m_id, seq)
        self.assertIsNotNone(res_command, "The result of send command is none")
        session_info, command_response = (res_command.session_info, res_command.payload)
        self.assertIsNotNone(session_info, "The session information is none")
        self.assertIsNotNone(command_response, "The result of send command is none")"""

    """def test_retrieve_pnr(self):
        m_id = None
        pnr = "Q68EFX"
        res_retrieve = self.client.get_reservation(pnr, m_id, True)
        self.assertIsNotNone(res_retrieve)
        session = res_retrieve.session_info
        self.assertIsNotNone(session)
        # self.assertTrue(session.session_ended)
        reservation = res_retrieve.payload
        self.assertIsNotNone(reservation)"""

    """def test_price_ok(self):
        m_id = None
        pnr = "Q68EFX"
        res_retrieve = self.client.get_reservation(pnr, m_id, True)
        self.assertIsNotNone(res_retrieve)
        session = res_retrieve.session_info
        self.assertIsNotNone(session)
        self.assertFalse(session.session_ended)
        res_price = self.client.fare_price_pnr_with_booking_class(session.message_id)
        self.assertIsNotNone(res_price)
        fares = res_price.payload
        self.assertIsNotNone(fares)
        if len(fares) >= 1:
            first_fare = fares[0]
            self.assertIsInstance(first_fare, Fare)"""

    # def test_price_past_date(self):
    #     m_id = None
    #     pnr = "WKHPRE"
    #     res_retrieve = self.client.get_reservation(pnr, m_id, True)
    #     self.assertIsNotNone(res_retrieve)
    #     session = res_retrieve.session_info
    #     self.assertIsNotNone(session)
    #     self.assertFalse(session.session_ended)
    #     res_price = self.client.fare_price_pnr_with_booking_class(session.message_id)
    #     self.assertIsNotNone(res_price)
    #     app_error = res_price.application_error
    #     self.assertIsNotNone(app_error)
    #     self.assertIsInstance(app_error, ApplicationError)
    #     self.assertEqual(app_error.error_code, "3024")

    def test_end_session(self):
        res_command = self.client.send_command("HELP")
        self.assertIsNotNone(res_command)
        session = res_command.session_info
        self.assertIsNotNone(session)
        self.assertFalse(session.session_ended)
        res_end_session = self.client.end_session(session.message_id)
        self.assertIsNotNone(res_end_session)
        session = res_end_session.session_info
        self.assertIsNotNone(session)
        self.assertTrue(session.session_ended)

    def test_end_session_not_exists(self):
        self.assertRaises(NoSessionError, self.client.end_session, "fake-message-id")

    """
    def test_create_tst(self):

        m_id = None
        pnr = "Q68EFX"
        res_retrieve = self.client.get_reservation(pnr, m_id, True)
        self.assertIsNotNone(res_retrieve)
        session = res_retrieve.session_info
        self.assertIsNotNone(session)
        self.assertFalse(session.session_ended)

        #     res_price = self.client.fare_price_pnr_with_booking_class(session.message_id)
        #     self.assertIsNotNone(res_price)
        #     session = res_price.session_info
        #     self.assertIsNotNone(session)
        #     self.assertFalse(session.session_ended)
        #     res_price = res_price.payload
        #     self.assertIsInstance(res_price, list)
        #     if len(res_price) >= 1:
        #         my_fare: Fare = res_price[0]
        #         self.assertIsInstance(my_fare, Fare)

        res_tst = self.client.ticket_create_tst_from_price(session.message_id, my_fare.fare_reference)
        self.assertIsNotNone(res_tst)
        session = res_tst.session_info
        self.assertIsNotNone(session)
        self.assertFalse(session.session_ended)
        res_tst = res_tst.payload
        self.assertIsNotNone(res_tst)
        """

    def test_create_pnr(self):
        search_results = self.client.send_command("AN11OCTLONTYO")
        message_id = search_results.session_info.message_id
        self.client.send_command("SS1Y1", message_id)
        self.client.send_command("NM1DIALLO/AMADOU", message_id)
        self.client.send_command("AP PAX CTC DEL 91 9865621231", message_id)
        self.client.send_command("APE AWIILLIAMS@BINGO.COM", message_id)
        self.client.send_command("TKOK", message_id)
        self.client.send_command("FXP/R,UP", message_id)
        self.client.send_command("RFAGENT", message_id)
        self.client.send_command("FP*CHEQUE", message_id)
        response_data = self.client.create_pnr(message_id)
        pnr = response_data.payload["pnr_header"].controle_number
        print("é")
        self.assertEqual(len(pnr), 6)
        print("me")


if __name__ == "__main__":
    unittest.main()
