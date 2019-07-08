# coding: utf-8
__author__ = "Mouhamad Ndiankho THIAM"
__copyright__ = "Copyright 2019, CTS"
__credits__ = ["Mouhamad Ndiankho THIAM", "Demba FALL", "Saliou"]
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Mouhamad Ndiankho THIAM"
__email__ = "mohamed@ctsfares.com"
__status__ = "Development"

import requests
from ..core import xmlparser

from .errors import ClientError, ServerError
from .xmlbuilders.builder import AmadeusXMLBuilder
from .amadeus_types import AmadeusSessionInfo


class AmadeusClient:
    """
        This is the main class to make calls to Amadeus API
    """
    def __init__(self, endpoint: str, username: str, password: str, office_id: str, wsap: str):
        self.endpoint = endpoint
        self.username = username
        self.password = password
        self.office_id = office_id
        self.xmlbuilder: AmadeusXMLBuilder = AmadeusXMLBuilder(endpoint, username, password, office_id, wsap)
        self.header_template = {'Content-Type': 'text/xml;charset=UTF-8', 'Accept-Encoding': 'gzip,deflate'}

    def __request_wrapper(self, method_name, request_data, soap_action):
        """
            This wrapper method helps wrap request with:
            1- creating request and calling it
            2- read status code
            3- look status code and handle exceptions
            4- parse response and return it
        """
        headers = self.header_template
        headers["SOAPAction"] = soap_action
        response = requests.post(self.endpoint, data=request_data, headers=headers)
        status = response.status_code
        print(f"{method_name} status: {status}")
        response_data = xmlparser.parse_xml(response.content)
        if status == 500:
            faultcode, faultstring = xmlparser.extract_single_elements(response_data, "//faultcode/text()", "//faultstring/text()")
            print(f"faultcode: {faultcode}, faultstring: {faultstring}")
            raise ServerError(status, faultcode, faultstring)
        elif status == 400:
            raise ClientError(status, "Client Error")
        return response_data

    def start_new_session(self):
        """
            This method starts a new session to Amadeus
        """
        request_data = self.xmlbuilder.start_transaction(None, self.office_id, self.username, self.password, None, None)
        response_data = self.__request_wrapper("start_new_session", request_data, 'http://webservices.amadeus.com/VLSSOQ_04_1_1A')
        seq, tok, ses = xmlparser.extract_single_elements(response_data, "//*[local-name()='SequenceNumber']/text()", "//*[local-name()='SecurityToken']/text()", "//*[local-name()='SessionId']/text()")
        return AmadeusSessionInfo(tok, seq, ses)

    def fare_master_pricer_travel_board_search(self, origin, destination, departure_date, arrival_date):
        """
            A method for searching prices of an itinerary
        """
        request_data = self.xmlbuilder.fare_master_pricer_travel_board_search(self.office_id, origin, destination, departure_date, arrival_date)
        response_data = self.__request_wrapper("fare_master_pricer_travel_board_search", request_data, 'http://webservices.amadeus.com/FMPTBQ_18_1_1A')
        return response_data

    def fare_price_pnr_with_booking_class(self, message_id, session_id, sequence_number, security_token):
        """
            Price a PNR with a booking class.
            The PNR is supposed to be supplied in the session on a previous call
        """
        request_data = self.xmlbuilder.fare_price_pnr_with_booking_class(message_id, session_id, sequence_number, security_token)
        response_data = self.__request_wrapper("fare_price_pnr_with_booking_class", request_data, 'http://webservices.amadeus.com/TPCBRQ_18_1_1A')
        return response_data