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

from .response_extractor import PriceSearchExtractor, ErrorExtractor, SessionExtractor, PricePNRExtractor, AddMultiElementExtractor
from .errors import ClientError, ServerError
from .xmlbuilders.builder import AmadeusXMLBuilder
from .sessions import SessionHolder


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
        self.session_holder = SessionHolder()
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
        if status == 500:
            faultcode, faultstring = ErrorExtractor(response.content).extract()
            print(f"faultcode: {faultcode}, faultstring: {faultstring}")
            raise ServerError(status, faultcode, faultstring)
        elif status == 400:
            raise ClientError(status, "Client Error")
        return response.content

    def start_new_session(self):
        """
            This method starts a new session to Amadeus.
        """
        request_data = self.xmlbuilder.start_transaction(None, self.office_id, self.username, self.password, None, None)
        response_data = self.__request_wrapper("start_new_session", request_data, 'http://webservices.amadeus.com/VLSSOQ_04_1_1A')
        return SessionExtractor(response_data).extract()

    def end_transaction(self, message_id, session_id, sequence_number, security_token):
        request_data = self.xmlbuilder.end_transaction(message_id, session_id, sequence_number, security_token)
        response_data = self.__request_wrapper("end_transaction", request_data, 'http://webservices.amadeus.com/VLSSOQ_04_1_1A')
        return response_data

    def fare_master_pricer_travel_board_search(self, origin, destination, departure_date, arrival_date):
        """
            A method for searching prices of an itinerary.
        """
        request_data = self.xmlbuilder.fare_master_pricer_travel_board_search(self.office_id, origin, destination, departure_date, arrival_date)
        response_data = self.__request_wrapper("fare_master_pricer_travel_board_search", request_data, 'http://webservices.amadeus.com/FMPTBQ_18_1_1A')
        extractor = PriceSearchExtractor(response_data)
        return extractor.extract()

    def sell_from_recommandation(self, itineraries):
        request_data = self.xmlbuilder.sell_from_recomendation(itineraries)
        response_data = self.__request_wrapper("sell_from_recommandation", request_data, 'http://webservices.amadeus.com/ITAREQ_05_2_IA')
        return SessionExtractor(response_data).extract()

    def fare_price_pnr_with_booking_class(self, message_id, session_id, sequence_number, security_token):
        """
            Price a PNR with a booking class.
            The PNR is supposed to be supplied in the session on a previous call.
        """
        request_data = self.xmlbuilder.fare_price_pnr_with_booking_class(message_id, session_id, sequence_number, security_token)
        # print(request_data)
        response_data = self.__request_wrapper("fare_price_pnr_with_booking_class", request_data, 'http://webservices.amadeus.com/TPCBRQ_18_1_1A')
        print(response_data)
        return PricePNRExtractor(response_data).extract()

    def ticket_create_TST_from_price(self, message_id, session_id, sequence_number, security_token, tst_reference):
        """
            Creates a TST from TST reference
        """
        request_data = self.xmlbuilder.ticket_create_TST_from_price(message_id, session_id, sequence_number, security_token, tst_reference)
        response_data = self.__request_wrapper("ticket_create_TST_from_pricing", request_data, 'http://webservices.amadeus.com/TAUTCQ_04_1_1A')
        return response_data

    def add_passenger_info(self, office_id, message_id, session_id, sequence_number, security_token, infos):
        """
            add passenger info and create the PNR
        """
        request_data = self.xmlbuilder.add_passenger_info(office_id, message_id, session_id, sequence_number, security_token, infos)
        # print(request_data)
        response_data = self.__request_wrapper("add_passenger_info", request_data, 'http://webservices.amadeus.com/PNRADD_17_1_1A')
        return AddMultiElementExtractor(response_data).extract()


