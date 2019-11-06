import os
import json
import unittest
from pygds.sabre.client import SabreClient
from pygds.env_settings import get_setting
from pygds.core.security_utils import decode_base64
from pygds.sabre.jsonbuilders.create_pnr import PassengerFare, FlightSegment, CreatePnrRequest
# from pygds.amadeus.amadeus_types import GdsResponse
# from pygds.core.helpers import get_data_from_json as from_json
# from pygds.sabre.json_parsers.create_passenger_name_record import CreatePnrInfo


class ClientCan(unittest.TestCase):
    """ This class will test all our function on the client side """

    def setUp(self) -> None:
        self.pcc = get_setting("SABRE_PCC")
        self.username = get_setting("SABRE_USERNAME")
        self.password = decode_base64(get_setting("SABRE_PASSWORD"))
        self.rest_url = "https://api.havail.sabre.com"
        self.client = SabreClient("https://webservices3.sabre.com", self.rest_url, self.username, self.password, self.pcc, False)
        self.token = None
        base_path = os.path.dirname(os.path.abspath(__file__))
        create_pnr_request = os.path.join(base_path, "resources/createpnr/create_pnr_request_com.json")
        create_pnr_request_response = os.path.join(base_path, "resources/createpnr/request_net_res.json")

        with open(create_pnr_request) as j:
            self.create_pnr_request_json = json.load(j)
        with open(create_pnr_request_response) as r:
            self.create_pnr_request_json_res = json.load(r)

    def test_create_pnr_request_json(self):
        pax_list = []
        for pax in self.create_pnr_request_json['Passengers']:
            passenger = PassengerFare()
            passenger.name_number = pax['NameNumber']
            passenger.given_name = pax['GivenName']
            passenger.surname = pax['Surname']
            passenger.date_of_birth = pax['DateOfBirth']
            passenger.gender = pax['Gender']
            passenger.passenger_type = pax['PassengerType']
            passenger.amount = pax['Amount']
            passenger.percent = pax['Percent']
            passenger.ticket_designator = pax['TicketDesignator']
            passenger.tour_code = pax['TourCode']
            passenger.total_fare = pax['TotalFare']
            passenger.service_fee = pax['ServiceFee']
            passenger.phone = pax['Phone']
            passenger.email = pax['Email']
            passenger.address = pax['Address']
            passenger.middle_name = pax['MiddleName']
            passenger.brand_id = None
            pax_list.append(passenger)
        segments = []
        for flight_segment in self.create_pnr_request_json['FlightSegment']:
            segment = FlightSegment()
            segment.arrival_date_time = flight_segment['ArrivalDateTime']
            segment.departure_date_time = flight_segment['DepartureDateTime']
            segment.flight_number = flight_segment['FlightNumber']
            segment.number_in_party = flight_segment['NumberInParty']
            segment.res_book_desig_code = flight_segment['ResBookDesigCode']
            segment.status = flight_segment['Status']
            segment.destination_location = flight_segment['DestinationLocation']
            segment.marketing_airline = flight_segment['MarketingAirline']
            segment.marriage_grp = flight_segment['MarriageGrp']
            segment.operating_airline = flight_segment['OperatingAirline']
            segment.origin_location = flight_segment['OriginLocation']
            segments.append(segment)
        create_pnr_object = CreatePnrRequest(segments, pax_list, self.create_pnr_request_json['Remarks'], self.create_pnr_request_json['TargetCity'], self.create_pnr_request_json['FareType'], self.create_pnr_request_json['CustomerIdentifier'], 'mbaye@ctsfares.com', self.create_pnr_request_json['LastTicketDate'])
        # print(create_pnr_object.to_dict())
        # create_pnr_builder = CreatePnrBuilder(create_pnr_object)
        # print(create_pnr_builder.to_dict())
        response = self.client.create_pnr_rq(self.token, True, create_pnr_object)
        self.assertIsNotNone(response)
        """
        self.assertIsInstance(response, GdsResponse)
        # self.assertIsNotNone(response.payload, GdsResponse)
        # self.assertIsInstance(response.payload, CreatePnrInfo)
        # self.assertEqual(from_json(response.payload.to_dict(), 'Status'), 'Complete')
        # self.assertIsInstance(from_json(response.payload.to_dict(), 'RecordLocator'), str)
        # self.assertIsInstance(from_json(response.payload.to_dict(), 'AirBook'), dict)
        # self.assertIsInstance(from_json(response.payload.to_dict(), 'AirPrice'), list)
        # self.assertIsInstance(from_json(response.payload.to_dict(), 'TravelItineraryRead'), dict)
        """


if __name__ == "__main__":
    unittest.main()
