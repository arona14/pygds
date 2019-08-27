import unittest
from pygds.env_settings import get_setting
from pygds.sabre.client import SabreClient
from pygds.core.security_utils import decode_base64
from pygds.amadeus.amadeus_types import GdsResponse
from pygds.core.helpers import get_data_from_json as from_json


class RebookingTest(unittest.TestCase):

    def setUp(self) -> None:
        self.pcc = get_setting("SABRE_PCC")
        self.username = get_setting("SABRE_USERNAME")
        self.password = decode_base64(get_setting("SABRE_PASSWORD"))
        self.rest_url = ""
        self.soap_url = "https://webservices3.sabre.com"
        self.client = SabreClient(self.soap_url, self.rest_url, self.username, self.password, self.pcc, False)

    def test_rebooking(self):
        display_pnr = self.client.get_reservation("TLRYVS", None)
        session_info = display_pnr.session_info
        if not session_info:
            print("No session info")
            return
        message_id = session_info.message_id
        self.assertIsNotNone(message_id)
        flight_segment = [
            {"origin": "DTW", "destination": "EWR", "departure_date_time": "2019-09-26T08:40:00", "arrival_date_time": "2019-09-26T10:29:00",
                "flight_number": "3526", "number_in_party": 2, "res_book_desig_code": "N", "operating_code": "UA",
                "marketing_code": "UA", "status": "NN"},

            {"origin": "EWR", "destination": "DTW", "departure_date_time": "2019-10-11T06:00:00", "arrival_date_time": "2019-10-11T08:00:00",
                "flight_number": "3598", "number_in_party": 2, "res_book_desig_code": "N", "operating_code": "UA",
                "marketing_code": "UA", "status": "NN"}

        ]
        pnr = 'ZIFVQD'
        rebooking = self.client.re_book_air_segment(message_id, flight_segment, pnr)
        self.assertIsNotNone(rebooking)
        self.assertIsInstance(rebooking, GdsResponse)
        self.assertEqual(from_json(rebooking.payload, "status"), 'Complete')
        self.assertIsInstance(from_json(rebooking.payload, "air_book_rs"), dict)
        self.assertIsInstance(from_json(rebooking.payload, "travel_itinerary_read_rs"), dict)


if __name__ == "__main__":
    unittest.main()
