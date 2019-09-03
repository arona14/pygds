import os
import json
import unittest
from pygds.sabre.client import SabreClient
from pygds.env_settings import get_setting
from pygds.core.security_utils import decode_base64
from pygds.core.request import RequestedSegment, LowFareSearchRequest, TravellerNumbering
from pygds.sabre.jsonbuilders.builder import SabreJSONBuilder
# from pygds.sabre.jsonbuilders.search_builder import BFMBuilder


class ClientCan(unittest.TestCase):
    """ This class will test all our function on the client side """

    def setUp(self) -> None:
        self.pcc = get_setting("SABRE_PCC")
        self.username = get_setting("SABRE_USERNAME")
        self.password = decode_base64(get_setting("SABRE_PASSWORD"))
        self.rest_url = "https://api.havail.sabre.com"
        self.soap_url = "https://webservices3.sabre.com"
        self.client = SabreClient(self.soap_url, self.rest_url, self.username, self.password, self.pcc, False)
        base_path = os.path.dirname(os.path.abspath(__file__))
        json_path_pub = os.path.join(base_path, "resources/sfjb/request_builder_pub.json")
        json_path_net = os.path.join(base_path, "resources/sfjb/request_builder_net.json")

        with open(json_path_pub) as j:
            self.search_pub = json.load(j)
        with open(json_path_net) as j:
            self.search_net = json.load(j)

    def test_search_flight(self):
        segment1 = RequestedSegment("DTW", "NYC", "2019-09-10").to_data()
        segment2 = RequestedSegment("NYC", "DTW", "2019-09-21").to_data()

        segments = []
        segments.append(segment1)
        segments.append(segment2)

        travel_number = TravellerNumbering(2, 1, 0)
        my_request = LowFareSearchRequest(segments, "Y", "WR17", travel_number, [], "50ITINS", [], False, True, 2)
        print(my_request.to_data())
        my_request_pub = SabreJSONBuilder("Production").search_flight_builder(my_request, True, "PUB")
        self.assertIsInstance(my_request_pub, dict)
        self.assertIsInstance(my_request_pub["OTA_AirLowFareSearchRQ"]["POS"], dict)
        self.assertIsInstance(my_request_pub["OTA_AirLowFareSearchRQ"]["OriginDestinationInformation"], list)
        self.assertIsInstance(my_request_pub["OTA_AirLowFareSearchRQ"]["TravelPreferences"], dict)
        self.assertIsInstance(my_request_pub["OTA_AirLowFareSearchRQ"]["TravelerInfoSummary"], dict)
        self.assertIsInstance(my_request_pub["OTA_AirLowFareSearchRQ"]["TPA_Extensions"], dict)
        # self.assertEqual(self.search_pub, my_request_pub)

        my_request_net = SabreJSONBuilder("Production").search_flight_builder(my_request, True, "NET")
        self.assertIsInstance(my_request_net, dict)
        self.assertIsInstance(my_request_net["OTA_AirLowFareSearchRQ"]["POS"], dict)
        self.assertIsInstance(my_request_net["OTA_AirLowFareSearchRQ"]["OriginDestinationInformation"], list)
        self.assertIsInstance(my_request_net["OTA_AirLowFareSearchRQ"]["TravelPreferences"], dict)
        self.assertIsInstance(my_request_net["OTA_AirLowFareSearchRQ"]["TravelerInfoSummary"], dict)
        self.assertIsInstance(my_request_net["OTA_AirLowFareSearchRQ"]["TPA_Extensions"], dict)
        # self.assertEqual(self.search_net, my_request_net)
        # result = self.client.search_flight("modou", my_request, True, "PUB")
