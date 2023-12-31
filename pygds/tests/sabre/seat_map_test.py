import unittest
from pygds.sabre.client import SabreClient
from pygds.env_settings import get_setting
from pygds.core.security_utils import decode_base64
from pygds.core.types import FlightSeatMap, Passenger


class SeatMapTest(unittest.TestCase):

    def test_seat_map(self):
        # write exactly the same test as in previous example
        pcc = get_setting("SABRE_PCC")
        username = get_setting("SABRE_USERNAME")
        password = decode_base64(get_setting("SABRE_PASSWORD"))
        rest_url = "https://api.havail.sabre.com"
        soap_url = "https://webservices3.sabre.com"
        client = SabreClient(soap_url, rest_url, username, password, pcc, False)

        flight_info = FlightSeatMap()
        flight_info.origin = "DTW"
        flight_info.destination = "NYC"
        flight_info.operating_flight_number = "8800"
        flight_info.marketing_flight_number = "8800"
        flight_info.operating_code = "DL"
        flight_info.marketing_code = "DL"
        flight_info.currency_code = "USD"
        flight_info.depart_date = "10/10/2019"
        flight_info.arrival_date = "20/10/2019"
        passenger = Passenger()
        passenger.passenger_type = 'ADT'
        passenger.number_in_party = '1'
        passenger.first_name = 'ADUN'
        passenger.last_name = 'LECOQ'
        passenger.name_id = 1
        seat_map_xml = client.xml_builder.seap_map_rq(None, flight_info, [passenger])
        self.assertIsNotNone(seat_map_xml)
        self.assertIn("soapenv:Envelope", seat_map_xml)
        self.assertIn("<tag0:RequestType>Payload</tag0:RequestType>", seat_map_xml)
        self.assertIn("<eb:Service>EnhancedSeatMapRQ</eb:Service>", seat_map_xml)
        self.assertIn("<eb:Action>EnhancedSeatMapRQ</eb:Action>", seat_map_xml)
        self.assertIn("<tag0:DepartureDate>10/10/2019</tag0:DepartureDate>", seat_map_xml)
        self.assertIn("<tag0:Operating carrier=\"DL\">8800</tag0:Operating>", seat_map_xml)
        self.assertIn("<tag0:Marketing carrier=\"DL\">8800</tag0:Marketing>", seat_map_xml)


if __name__ == "__main__":
    unittest.main()
