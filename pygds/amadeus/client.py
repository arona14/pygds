# coding: utf-8
from typing import List
from pygds.amadeus.xml_parsers.retrive_pnr import GetPnrResponseExtractor
from pygds.core.price import PriceRequest
from pygds.core.types import TravellerNumbering, Itinerary
from pygds.errors.gdserrors import NoSessionError
from pygds.core.client import BaseClient
from pygds.amadeus.xml_parsers.response_extractor import PriceSearchExtractor, ErrorExtractor, SessionExtractor, \
    CommandReplyExtractor, PricePNRExtractor, AddMultiElementExtractor, CreateTstResponseExtractor, \
    IssueTicketResponseExtractor
from pygds.core.payment import FormOfPayment
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
        request_data = self.xml_builder.start_transaction(None, self.office_id, self.username, self.password, None,
                                                          None)
        response_data = self.__request_wrapper("start_new_session", request_data,
                                               'http://webservices.amadeus.com/VLSSLQ_06_1_1A')
        return SessionExtractor(response_data).extract()

    def end_session(self, message_id):
        """
        This is for ending a current session
        :param message_id: the message id associated to that session
        :return: A GdsResponse containing the session info
        """
        session_id, sequence_number, security_token = self.get_or_create_session_details(message_id)
        if not security_token:
            raise NoSessionError(message_id)
        request_data = self.xml_builder.end_session(message_id, session_id, sequence_number, security_token)
        response_data = self.__request_wrapper("start_new_session", request_data,
                                               'http://webservices.amadeus.com/VLSSOQ_04_1_1A')
        return SessionExtractor(response_data).extract()

    def get_reservation(self, record_locator: str, message_id: str = None, close_trx: bool = False):
        """
            Return the reservation data from PNR.
        """
        session_id, sequence_number, security_token = self.get_or_create_session_details(message_id)
        self.log.info(f"Retreive pnr '{record_locator}'.")
        request_data = self.xml_builder.get_reservation_builder(record_locator, message_id, session_id, sequence_number, security_token, close_trx)
        if security_token is None:
            self.log.warning("A new session will be created when retrieve pnr.")
        data = self.__request_wrapper("get_reservation", request_data, 'http://webservices.amadeus.com/PNRRET_17_1_1A')
        # print(data)
        response = GetPnrResponseExtractor(data).extract()
        self.add_session(response.session_info)
        return response

    def add_form_of_payment(self, message_id, form_of_payment, passenger_reference_type, passenger_reference_value,
                            form_of_payment_sequence_number, group_usage_attribute_type, fop: FormOfPayment):
        """
            This method adds a form of payment to a PNR.
            The session must exists and a current PNR defined.
        """
        session_id, sequence_number, security_token = self.get_or_create_session_details(message_id)
        request_data = self.xml_builder.add_form_of_payment_builder(
            message_id, session_id, sequence_number, security_token, form_of_payment, passenger_reference_type,
            passenger_reference_value, form_of_payment_sequence_number, group_usage_attribute_type,
            fop)
        response_data = self.__request_wrapper("add_form_of_payment", request_data,
                                               'http://webservices.amadeus.com/TFOPCQ_15_4_1A')
        return response_data

    def pnr_add_multi_element(self, session_id, sequence_number, security_token, message_id, option_code, segment_name,
                              identification, credit_card_code, account_number, expiry_date, currency_code):
        """
            This method modifies the elements of a PNR (passengers, etc.)
        """
        request_data = self.xml_builder.pnr_add_multi_element_builder(session_id, sequence_number, security_token,
                                                                      message_id, option_code, segment_name,
                                                                      identification, credit_card_code, account_number,
                                                                      expiry_date, currency_code)
        response_data = self.__request_wrapper("pnr_add_multi_element", request_data,
                                               'http://webservices.amadeus.com/PNRADD_17_1_1A')
        return response_data

    def ticketing_pnr(self, message_id, passenger_reference_type, passenger_reference_value):
        """
            PNR ticketing process.
        """
        session_id, sequence_number, security_token = self.get_or_create_session_details(message_id)
        request_data = self.xml_builder.ticket_pnr_builder(message_id, session_id, sequence_number, security_token,
                                                           passenger_reference_type, passenger_reference_value)
        response_data = self.__request_wrapper("ticketing_pnr", request_data,
                                               'http://webservices.amadeus.com/TTKTIQ_15_1_1A')
        final_result = IssueTicketResponseExtractor(response_data).extract()
        self.add_session(final_result.session_info)
        return final_result

    def issue_ticket_with_retrieve(self, message_id):
        session_id, sequence_number, security_token = self.get_or_create_session_details(message_id)
        if not session_id:
            raise NoSessionError(message_id)
        request_data = self.xml_builder.issue_ticket_retrieve(message_id, security_token, sequence_number, session_id)
        response_data = self.__request_wrapper("issue_ticket_with_retrieve", request_data,
                                               'http://webservices.amadeus.com/TTKTIQ_15_1_1A')
        final_result = IssueTicketResponseExtractor(response_data).extract()
        self.add_session(final_result.session_info)
        return final_result

    def fare_master_pricer_travel_board_search(self, origin, destination, departure_date, arrival_date,
                                               numbering: TravellerNumbering):
        """
            A method for searching prices of an itinerary.
        """
        request_data = self.xml_builder.fare_master_pricer_travel_board_search(self.office_id, origin, destination,
                                                                               departure_date, arrival_date, numbering)
        response_data = self.__request_wrapper("fare_master_pricer_travel_board_search", request_data,
                                               'http://webservices.amadeus.com/FMPTBQ_18_1_1A')
        extractor = PriceSearchExtractor(response_data)
        return extractor.extract()

    def fare_informative_price_without_pnr(self, numbering: TravellerNumbering, itineraries: List[Itinerary]):
        request_data = self.xmlbuilder.fare_informative_price_without_pnr(numbering, itineraries)
        response_data = self.__request_wrapper("fare_informative_price_without_pnr", request_data,
                                               'http://webservices.amadeus.com/TIPNRQ_18_1_1A')
        extractor = PriceSearchExtractor(response_data)
        return extractor.extract()

    def fare_check_rules(self):
        return None

    def sell_from_recommandation(self, itineraries):
        request_data = self.xml_builder.sell_from_recomendation(itineraries)
        response_data = self.__request_wrapper("sell_from_recommandation", request_data,
                                               'http://webservices.amadeus.com/ITAREQ_05_2_IA')
        return SessionExtractor(response_data).extract()

    def fare_price_pnr_with_booking_class(self, office_id, message_id, session_id, sequence_number, security_token, pax_infos, price_request: PriceRequest = None):
        """
        Price a PNR with a booking class.
        The PNR is supposed to be supplied in the session on a previous call.
        :param message_id: The message id associated to
        :param price_request:
        :return:
        """
        # session_id, sequence_number, security_token = self.get_or_create_session_details(message_id)
        # if security_token is None:
        #     raise NoSessionError(message_id)
        request_data = self.xml_builder.fare_price_pnr_with_booking_class(message_id, session_id, sequence_number,
                                                                          security_token, price_request)
        response_data = self.__request_wrapper("fare_price_pnr_with_booking_class", request_data,
                                               'http://webservices.amadeus.com/TPCBRQ_18_1_1A')
        # print(response_data)
        final_response = PricePNRExtractor(response_data).extract()
        self.add_session(final_response.session_info)
        return final_response

    def ticket_create_tst_from_price(self, message_id, tst_reference):
        """
            Creates a TST from TST reference
        """
        session_id, sequence_number, security_token = self.get_or_create_session_details(message_id)
        if security_token is None:
            raise NoSessionError(message_id)
        request_data = self.xml_builder.ticket_create_tst_from_price(message_id, session_id, sequence_number,
                                                                     security_token, tst_reference)
        response_data = self.__request_wrapper("ticket_create_TST_from_pricing", request_data,
                                               'http://webservices.amadeus.com/TAUTCQ_04_1_1A')
        final_response = CreateTstResponseExtractor(response_data).extract()
        self.add_session(final_response.session_info)
        return final_response

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
        request_data = self.xml_builder.add_passenger_info(office_id, message_id, session_id, sequence_number,
                                                           security_token, infos)
        response_data = self.__request_wrapper("add_passenger_info", request_data,
                                               'http://webservices.amadeus.com/PNRADD_17_1_1A')
        # print(response_data)
        return AddMultiElementExtractor(response_data).extract()
