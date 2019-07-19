# coding: utf-8
from typing import List

from pygds.core.types import TravellerNumbering, Itinerary

__author__ = "Mouhamad Ndiankho THIAM"
__copyright__ = "Copyright 2019, CTS"
__credits__ = ["Mouhamad Ndiankho THIAM", "Demba FALL", "Saliou"]
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Mouhamad Ndiankho THIAM"
__email__ = "mohamed@ctsfares.com"
__status__ = "Development"

from pygds.core.client import BaseClient
from .response_extractor import PriceSearchExtractor, ErrorExtractor, SessionExtractor, CommandReplyExtractor, PricePNRExtractor, AddMultiElementExtractor
from .errors import ClientError, ServerError
from .xmlbuilders.builder import AmadeusXMLBuilder


class AmadeusClient(BaseClient):
    """
        Create a new Amadeus client that is independent to do every request permitted by it's access level.
        :param endpoint: The url of the endpoint. It can be on test, or production
        :param username: The username to authenticate to the Amadeus Server
        :param password: The password to authenticate to the Amadeus Server
        :param office_id: The office_id (or PCC)
        :param wsap: The Amadeus Wep Service Access Point
        :param debug: Telling if the client is debugging requests and responses.
    """
    def __init__(self, endpoint: str, username: str, password: str, office_id: str, wsap: str, debug: bool = False):
        super().__init__(endpoint, username, password, office_id, debug)
        self.xml_builder: AmadeusXMLBuilder = AmadeusXMLBuilder(endpoint, username, password, office_id, wsap)

    def __request_wrapper(self, method_name: str, request_data: str, soap_action: str):
        """
        This wrapper method helps wrap request with:
            1- creating request and calling it
            2- read status code
            3- look status code and handle exceptions
            4- parse response and return it
        :param method_name: The name of the method. useful for logging purposes
        :param request_data: the XML containing the request data
        :param soap_action: The SAOP action
        :return: the contain of the response
        """
        response = self._request_wrapper(request_data, soap_action)
        status = response.status_code
        if self.is_debugging:
            self.log.debug(request_data)
            self.log.debug(response.content)
            self.log.debug(f"{method_name} status: {status}")
        if status == 500:
            error = ErrorExtractor(response.content).extract()
            sess, (faultcode, faultstring) = error.session_info, error.payload
            self.log.error(f"faultcode: {faultcode}, faultstring: {faultstring}")
            raise ServerError(sess, status, faultcode, faultstring)
        elif status == 400:
            sess = SessionExtractor(response.content).extract()
            raise ClientError(sess, status, "Client Error")
        return response.content

    def start_new_session(self):
        """
            This method starts a new session to Amadeus.
        """
        request_data = self.xml_builder.start_transaction(None, self.office_id, self.username, self.password, None, None)
        response_data = self.__request_wrapper("start_new_session", request_data, 'http://webservices.amadeus.com/VLSSLQ_06_1_1A')
        return SessionExtractor(response_data).extract()

    def end_session(self, message_id):
        session_id, sequence_number, security_token = self.get_or_create_session_details(message_id)
        request_data = self.xml_builder.end_session(message_id, session_id, sequence_number, security_token)
        response_data = self.__request_wrapper("start_new_session", request_data, 'http://webservices.amadeus.com/VLSSOQ_04_1_1A')
        return SessionExtractor(response_data).extract()

    def fare_master_pricer_travel_board_search(self, origin, destination, departure_date, arrival_date):
        """
            A method for searching prices of an itinerary.
        """
        request_data = self.xml_builder.fare_master_pricer_travel_board_search(self.office_id, origin, destination, departure_date, arrival_date)
        response_data = self.__request_wrapper("fare_master_pricer_travel_board_search", request_data, 'http://webservices.amadeus.com/FMPTBQ_18_1_1A')
        # print(response_data)
        extractor = PriceSearchExtractor(response_data)
        return extractor.extract()

    def fare_informative_price_without_pnr(self, numbering: TravellerNumbering, itineraries: List[Itinerary]):
        request_data = self.xmlbuilder.fare_informative_price_without_pnr(numbering, itineraries)
        response_data = self.__request_wrapper("fare_informative_price_without_pnr", request_data, 'http://webservices.amadeus.com/TIPNRQ_18_1_1A')
        print(response_data)
        extractor = PriceSearchExtractor(response_data)
        return extractor.extract()


    def fare_check_rules(self):
        return None

    def sell_from_recommandation(self, itineraries):
        request_data = self.xmlbuilder.sell_from_recomendation(itineraries)
        response_data = self.__request_wrapper("sell_from_recommandation", request_data, 'http://webservices.amadeus.com/ITAREQ_05_2_IA')
        # print(response_data)
        return SessionExtractor(response_data).extract()

    def fare_price_pnr_with_booking_class(self, message_id, session_id, sequence_number, security_token):
        """
            Price a PNR with a booking class.
            The PNR is supposed to be supplied in the session on a previous call.
        """
        session_id, sequence_number, security_token = self.get_or_create_session_details(message_id)
        request_data = self.xml_builder.fare_price_pnr_with_booking_class(message_id, session_id, sequence_number, security_token)
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

    def send_command(self, command: str, message_id: str = None, close_trx: bool = False):
        """
        Send a command to Amadeus API
        :param command: the command to send as str
        :param message_id: The message id as str. Can be None if starting a new session
        :param close_trx: boolean telling if we are ending or not the current session
        :return: GdsResponse with the response of the command as payload
        """
        session_id, sequence_number, security_token = self.get_or_create_session_details(message_id)
        self.log.info(f"Sending command '{command}' to Amadeus server.")
        request_data = self.xml_builder.send_command(command, message_id, session_id, sequence_number, security_token,
                                                     close_trx)
        if security_token is None:
            self.log.warning("A new session will be created when sending the command.")
        data = self.__request_wrapper("send_command", request_data, 'http://webservices.amadeus.com/HSFREQ_07_3_1A')
        res = CommandReplyExtractor(data).extract()
        self.add_session(res.session_info)
        return res

    def add_passenger_info(self, office_id, message_id, session_id, sequence_number, security_token, infos):
        """
            add passenger info and create the PNR
        """
        request_data = self.xmlbuilder.add_passenger_info(office_id, message_id, session_id, sequence_number, security_token, infos)
        # print(request_data)
        response_data = self.__request_wrapper("add_passenger_info", request_data, 'http://webservices.amadeus.com/PNRADD_17_1_1A')
        return AddMultiElementExtractor(response_data).extract()

