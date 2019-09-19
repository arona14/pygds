from unittest import TestCase
import unittest
from pygds.amadeus.client import AmadeusClient
# from pygds.core.app_error import ApplicationError
from pygds.env_settings import get_setting
from pygds.core.price import PriceRequest
from pygds.errors.gdserrors import NoSessionError
from pygds.core.types import TravellerInfo, ReservationInfo


class ClientCan(TestCase):
    def setUp(self) -> None:
        endpoint = get_setting("AMADEUS_ENDPOINT_URL")
        username = get_setting("AMADEUS_USERNAME")
        password = get_setting("AMADEUS_PASSWORD")
        self.office_id = get_setting("AMADEUS_OFFICE_ID")
        wsap = get_setting("AMADEUS_WSAP")
        self.client = AmadeusClient(endpoint, username, password, self.office_id, wsap, False)

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

    def test_add_passenger(self):
        search_results = self.client.send_command("AN12OCTTRZKUL/KY/B2")
        message_id = search_results.session_info.message_id
        self.client.send_command("SS2Y1", message_id)
        traveller_infos = [TravellerInfo(1, "Mouhamad", "JJ", "FALL", "03121990", "ADT"), TravellerInfo(2, "Amadou", "JJ", "Diallo", "03121990", "ADT")]
        reservation_info = ReservationInfo(traveller_infos, "776656986", "785679876", "diallo@gmail.com")
        passenger_info_response = self.client.add_passenger_info(self.office_id, message_id, reservation_info)
        self.assertEqual(len(passenger_info_response.payload["passengers"]), 2)
        self.client.end_session(message_id)

    """ def test_price_ok(self):

        message_id = self.sub_processing()
        response_data = self.client.create_pnr(message_id)
        self.client.end_session(message_id)
        pnr = response_data.payload["pnr_header"].controle_number
        self.assertEqual(len(pnr), 6)
        res_reservation = self.client.get_reservation(pnr, None, False)
        res_reservation, message_id = res_reservation.payload, res_reservation.session_info.message_id
        seg_refs = []
        pax_refs = []
        for seg in res_reservation["itineraries"]:
            seg_refs.append(seg.segment_reference)
        for pax in res_reservation["passengers"]:
            pax_refs.append(pax.name_id)
        price_request = PriceRequest(pax_refs, seg_refs)
        res_price = self.client.fare_price_pnr_with_booking_class(message_id, price_request)
        self.client.end_session(message_id)
        fare_reference = res_price.payload[0].fare_reference
        self.assertIsNotNone(fare_reference)"""

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

    """" def test_create_pnr(self):
        message_id = self.sub_processing()
        response_data = self.client.create_pnr(message_id)
        self.client.end_session(message_id)
        pnr = response_data.payload["pnr_header"].controle_number
        self.assertEqual(len(pnr), 6)"""

    def sub_processing(self):
        search_results = self.client.send_command("AN12OCTTRZKUL/KY")
        message_id = search_results.session_info.message_id
        self.client.send_command("SS1Y1", message_id)
        self.client.send_command("NM1DIALLO/AMADOU", message_id)
        self.client.send_command("AP PAX CTC DEL 91 9865621231", message_id)
        self.client.send_command("APE AWIILLIAMS@BINGO.COM", message_id)
        self.client.send_command("TKOK", message_id)
        self.client.send_command("RFTHIAM", message_id)
        self.client.send_command("FP*CHEQUE", message_id)
        return message_id


if __name__ == "__main__":
    unittest.main()
