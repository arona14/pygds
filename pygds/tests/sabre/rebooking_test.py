import unittest
from pygds.env_settings import get_setting
from pygds.sabre.client import SabreClient
from pygds.core.security_utils import decode_base64
from pygds.amadeus.amadeus_types import GdsResponse
from pygds.core.rebook import RebookInfo


class RebookingTest(unittest.TestCase):

    def setUp(self) -> None:
        self.pcc = get_setting("SABRE_PCC")
        self.username = get_setting("SABRE_USERNAME")
        self.password = decode_base64(get_setting("SABRE_PASSWORD"))
        self.rest_url = ""
        self.soap_url = "https://webservices3.sabre.com"
        self.client = SabreClient(self.soap_url, self.rest_url, self.username, self.password, self.pcc, False)

    def test_rebooking(self):
        self.client.get_reservation(None, False, "SMZEKA")
        flight_segment = [
            {"origin": "DTW", "destination": "EWR", "departure_date_time": "2019-09-26T08:40:00", "arrival_date_time": "2019-09-26T10:29:00",
                "flight_number": "3526", "number_in_party": 2, "res_book_desig_code": "N", "operating_code": "UA",
                "marketing_code": "UA", "status": "NN"},

            {"origin": "EWR", "destination": "DTW", "departure_date_time": "2019-10-11T06:00:00", "arrival_date_time": "2019-10-11T08:00:00",
                "flight_number": "3598", "number_in_party": 2, "res_book_desig_code": "N", "operating_code": "UA",
                "marketing_code": "UA", "status": "NN"}

        ]
        pnr = 'SMZEKA'
        rebooking = self.client.re_book_air_segment(None, True, flight_segment, pnr)
        self.assertIsNotNone(rebooking)
        self.assertIsInstance(rebooking, GdsResponse)
        self.assertIsInstance(rebooking.payload, RebookInfo)
        # self.assertEqual(rebooking.payload.status, 'Complete')
        self.assertIsInstance(rebooking.payload.air_book_rs, dict)
        self.assertIsInstance(rebooking.payload.travel_itinerary_read_rs, dict)


if __name__ == "__main__":
    unittest.main()
