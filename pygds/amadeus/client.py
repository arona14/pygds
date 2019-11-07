# coding: utf-8
from .xmlbuilders.builder import AmadeusXMLBuilder
from .errors import ClientError, ServerError
from pygds.core.payment import FormOfPayment, CreditCard, CheckPayment
from typing import List
from pygds.amadeus.xml_parsers.retrive_pnr import GetPnrResponseExtractor
from pygds.core.file_logger import FileLogger
from pygds.core.price import PriceRequest
from pygds.core.sessions import SessionInfo
from pygds.core.types import TravellerNumbering, Itinerary, Recommandation
from pygds.core.request import LowFareSearchRequest
from pygds.errors.gdserrors import NoSessionError
from pygds.core.client import BaseClient
from pygds.amadeus.xml_parsers.response_extractor import PriceSearchExtractor, ErrorExtractor, SessionExtractor, \
    CommandReplyExtractor, PricePNRExtractor, CreateTstResponseExtractor, \
    IssueTicketResponseExtractor, CancelPnrExtractor, QueueExtractor, InformativePricingWithoutPnrExtractor, \
    VoidTicketExtractor, UpdatePassengers


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
    # log = log_handler.get_logger("test_all")

    def __init__(self, endpoint: str, username: str, password: str, office_id: str, wsap: str, debug: bool = False):
        super().__init__(endpoint, username, password, office_id, debug)
        self.xml_builder: AmadeusXMLBuilder = AmadeusXMLBuilder(endpoint, username, password, office_id, wsap)
        self.file_logger = FileLogger()

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
            self.file_logger.log_data(request_data, f"{method_name}_request.xml", False, True)
            self.log.debug(response.content)
            self.file_logger.log_data(response.content, f"{method_name}_response.xml", True, False)
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

    def close_session(self, message_id):
        """
        This is for ending a current session
        :param message_id: the message id associated to that session
        :return: A GdsResponse containing the session info
        """
        session_id, sequence_number, security_token = self.get_or_create_session_details(message_id)
        if not security_token:
            raise NoSessionError(message_id)
        request_data = self.xml_builder.end_session(message_id, session_id, sequence_number, security_token)
        response_data = self.__request_wrapper("end_new_session", request_data,
                                               'http://webservices.amadeus.com/VLSSOQ_04_1_1A')
        response = SessionExtractor(response_data).extract()
        self.session_holder.remove_session(message_id)
        return response

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
        response = GetPnrResponseExtractor(data).extract()
        self.add_session(response.session_info)
        return response

    def add_form_of_payment(self, message_id: str, fop: FormOfPayment, segment_refs: List[str], pax_refs: List[str], inf_refs: List[str], fop_sequence_number: str):
        """
            This method adds a form of payment to a PNR.
            The session must exists and a current PNR defined.
        """
        session_id, sequence_number, security_token = self.get_or_create_session_details(message_id)
        if not security_token:
            raise NoSessionError(message_id)
        request_data = self.xml_builder.add_form_of_payment_builder(
            message_id, session_id, sequence_number, security_token, fop, segment_refs, pax_refs, inf_refs, fop_sequence_number)
        if isinstance(fop, (CreditCard, CheckPayment)):
            response_data = self.__request_wrapper("add_form_of_payment", request_data,
                                                   'http://webservices.amadeus.com/TFOPCQ_15_4_1A')
        else:
            response_data = self.__request_wrapper("add_form_of_payment", request_data,
                                                   'http://webservices.amadeus.com/PNRADD_17_1_1A')

        session_info = SessionExtractor(response_data).extract()
        self.add_session(session_info.session_info)
        return session_info

    def pnr_add_multi_element(self, message_id, option_code, segment_name):
        """
            This method modifies the elements of a PNR (passengers, etc.)
        """
        session_id, sequence_number, security_token = self.get_or_create_session_details(message_id)
        if not security_token:
            raise NoSessionError(message_id)
        request_data = self.xml_builder.pnr_add_multi_element_builder(session_id, sequence_number, security_token,
                                                                      message_id, option_code, segment_name)
        response_data = self.__request_wrapper("pnr_add_multi_element", request_data,
                                               'http://webservices.amadeus.com/PNRADD_17_1_1A')
        response = GetPnrResponseExtractor(response_data).extract()
        self.add_session(response.session_info)
        return response

    def pnr_add_multi_for_pax_info_element(self, message_id, email_content, passenger_id, office_id):
        """
            This method modifies the elements of a PNR (passengers, etc.)
        """
        session_id, sequence_number, security_token = self.get_or_create_session_details(message_id)
        if not security_token:
            raise NoSessionError(message_id)
        request_data = self.xml_builder.pnr_add_multi_element_for_pax_info_builder(session_id, sequence_number, security_token,
                                                                                   message_id, email_content, passenger_id, office_id)
        response_data = self.__request_wrapper("pnr_add_multi_for_pax_info_element", request_data,
                                               'http://webservices.amadeus.com/PNRADD_17_1_1A')
        # print(response_data)
        return UpdatePassengers(response_data).extract()

    def cancel_information_passenger(self, reference, message_id):
        """
            This method modifies the elements of a PNR (passengers, etc.)
        """
        session_id, sequence_number, security_token = self.get_or_create_session_details(message_id)
        if not security_token:
            raise NoSessionError(message_id)
        request_data = self.xml_builder.cancel_information_passenger(session_id, sequence_number, security_token,
                                                                     message_id, reference)
        response_data = self.__request_wrapper("cancel information passenger", request_data,
                                               'http://webservices.amadeus.com/PNRXCL_14_2_1A')
        # print(response_data)
        return SessionExtractor(response_data).extract()

    def ticketing_pnr(self, message_id, passenger_reference_type, passenger_reference_value):
        """
            PNR ticketing process.
        """
        session_id, sequence_number, security_token = self.get_or_create_session_details(message_id)
        if not security_token:
            raise NoSessionError(message_id)
        request_data = self.xml_builder.ticket_pnr_builder(message_id, session_id, sequence_number, security_token,
                                                           passenger_reference_type, passenger_reference_value)
        response_data = self.__request_wrapper("ticketing_pnr", request_data,
                                               'http://webservices.amadeus.com/TTKTIQ_15_1_1A')
        print(response_data)
        final_result = IssueTicketResponseExtractor(response_data).extract()
        self.add_session(final_result.session_info)
        return final_result

    def issue_ticket_with_retrieve(self, message_id, tst_refs: List[str], pax_refs: List[str]):
        session_id, sequence_number, security_token = self.get_or_create_session_details(message_id)
        if not session_id:
            raise NoSessionError(message_id)
        request_data = self.xml_builder.issue_ticket_retrieve(message_id, security_token, sequence_number, session_id,
                                                              tst_refs)
        response_data = self.__request_wrapper("issue_ticket_with_retrieve", request_data,
                                               'http://webservices.amadeus.com/TTKTIQ_15_1_1A')
        final_result = IssueTicketResponseExtractor(response_data).extract()
        self.add_session(final_result.session_info)
        return final_result

    def fare_master_pricer_travel_board_search(self, low_fare_search: LowFareSearchRequest, currency_conversion=None, c_qualifier="RC"):
        """
            A method for searching prices of an itinerary.
        """
        request_data = self.xml_builder.fare_master_pricer_travel_board_search(self.office_id, low_fare_search, currency_conversion, c_qualifier)
        response_data = self.__request_wrapper("fare_master_pricer_travel_board_search", request_data,
                                               'http://webservices.amadeus.com/FMPTBQ_18_1_1A')
        response_data = PriceSearchExtractor(response_data).extract()
        # self.add_session(response_data.session_info)
        return response_data

    def fare_informative_price_without_pnr(self, message_id: str, numbering: TravellerNumbering, itineraries: List[Itinerary]):

        session_id, sequence_number, security_token = self.get_or_create_session_details(message_id)

        if security_token is None:
            raise NoSessionError(message_id)

        request_data = self.xml_builder.fare_informative_price_without_pnr(message_id, session_id, sequence_number,
                                                                           security_token, numbering, itineraries)
        response_data = self.__request_wrapper("fare_informative_price_without_pnr", request_data,
                                               'http://webservices.amadeus.com/TIPNRQ_18_1_1A')

        response_data = InformativePricingWithoutPnrExtractor(response_data).extract()
        self.add_session(response_data.session_info)

        return response_data

    def fare_informative_best_pricing_without_pnr(self, recommandation: Recommandation):

        request_data = self.xml_builder.fare_informative_best_price_without_pnr(recommandation)
        response_data = self.__request_wrapper("fare_informative_best_price_without_pnr", request_data,
                                               'http://webservices.amadeus.com/TIBNRQ_18_1_1A')

        response_data = SessionExtractor(response_data).extract()

        return response_data

    def fare_check_rules(self, message_id, line_number):
        session_id, sequence_number, security_token = self.get_or_create_session_details(message_id)
        if security_token is None:
            raise NoSessionError(message_id)
        request_data = self.xml_builder.fare_check_rules(message_id, session_id, sequence_number, security_token, line_number)
        response_data = self.__request_wrapper("check fare rules", request_data,
                                               'http://webservices.amadeus.com/FARQNQ_07_1_1A')
        return response_data

    def sell_from_recommandation(self, itineraries):
        request_data = self.xml_builder.sell_from_recomendation(itineraries)
        response_data = self.__request_wrapper("sell_from_recommandation", request_data,
                                               'http://webservices.amadeus.com/ITAREQ_05_2_IA')

        final_response = SessionExtractor(response_data).extract()

        self.add_session(final_response.session_info)
        return final_response

    def fare_price_pnr_with_booking_class(self, message_id, price_request: PriceRequest = None):
        """
        Price a PNR with a booking class.
        The PNR is supposed to be supplied in the session on a previous call.
        :param message_id: The message id associated to
        :param price_request:
        :return:
        """
        session_id, sequence_number, security_token = self.get_or_create_session_details(message_id)
        if security_token is None:
            raise NoSessionError(message_id)
        request_data = self.xml_builder.fare_price_pnr_with_booking_class(message_id, session_id, sequence_number,
                                                                          security_token, price_request)
        response_data = self.__request_wrapper("fare_price_pnr_with_booking_class", request_data,
                                               'http://webservices.amadeus.com/TPCBRQ_18_1_1A')
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

    def create_pnr(self, message_id):
        """
            create the PNR
        """
        session_id, sequence_number, security_token = self.get_or_create_session_details(message_id)
        if security_token is None:
            raise NoSessionError(message_id)
        request_data = self.xml_builder.create_pnr(message_id, session_id, sequence_number,
                                                   security_token)
        response_data = self.__request_wrapper("add_passenger_info", request_data,
                                               'http://webservices.amadeus.com/PNRADD_17_1_1A')
        return GetPnrResponseExtractor(response_data).extract()

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

    def add_passenger_info(self, office_id, message_id, infos, company_id):
        """
            add passenger info and create the PNR
        """
        session_id, sequence_number, security_token = self.get_or_create_session_details(message_id)
        if security_token is None:
            raise NoSessionError(message_id)
        request_data = self.xml_builder.add_passenger_info(office_id, message_id, session_id, sequence_number,
                                                           security_token, infos, company_id)
        response_data = self.__request_wrapper("add_passenger_info", request_data,
                                               'http://webservices.amadeus.com/PNRADD_17_1_1A')

        response_data = GetPnrResponseExtractor(response_data).extract()
        self.add_session(response_data.session_info)

        return response_data

    def pnr_add_ssr(self, message_id, passenger_ids, content, company_id):
        """
            add passenger info and create the PNR
        """
        session_id, sequence_number, security_token = self.get_or_create_session_details(message_id)
        if security_token is None:
            raise NoSessionError(message_id)
        request_data = self.xml_builder.pnr_add_ssr(session_id, sequence_number,
                                                    security_token, message_id, passenger_ids, content, company_id)
        response_data = self.__request_wrapper("add_ssr_in_pnr", request_data,
                                               'http://webservices.amadeus.com/PNRADD_17_1_1A')

        response_data = GetPnrResponseExtractor(response_data).extract()
        self.add_session(response_data.session_info)

        return response_data

    def queue_place_pnr(self, message_id: str, pnr: str, queues: List[str]):

        session_id, sequence_number, security_token = self.get_or_create_session_details(message_id)
        if security_token is None:
            raise NoSessionError(message_id)
        request_data = self.xml_builder.queue_place_pnr(message_id, session_id, sequence_number, security_token, pnr,
                                                        queues)
        response_data = self.__request_wrapper("queue_place_pnr", request_data, 'http://webservices.amadeus.com/QUQPCQ_03_1_1A')

        response_data = QueueExtractor(response_data).extract()
        self.add_session(response_data.session_info)
        return response_data
        return GetPnrResponseExtractor(response_data).extract()

    def issue_combined(self, message_id: str, passengers: List[str], segments: List[str], retrieve_pnr: bool):
        """
        This service is used to issue miscellaneous documents (MCO, TASF, XSB and/or EMD) and tickets SIMULTANEOUSLY.
        The ISSUANCE TRANSACTION is the process whereby the reservation and the pricing information are converted into
        contracts.
        CONTRACTS are issued for customers buying travel products; those contracts tie the customer to the travel
        provider (e.g. validating carrier of an airline product).
        :param message_id: str -> the message id
        :param passengers: List[str] -> List of passenger tattoos
        :param segments: List[str] -> List of segment tattoos
        :param retrieve_pnr: to tell if we will retrieve PNR again
        :return:
        """
        session_id, sequence_number, security_token = self.get_or_create_session_details(message_id)
        if security_token is None:
            raise NoSessionError(message_id)
        session_info = SessionInfo(security_token, sequence_number, session_id, message_id, False)
        request_data = self.xml_builder.issue_combined(session_info, passengers, segments, retrieve_pnr)
        response_data = self.__request_wrapper("issue_combined", request_data,
                                               'http://webservices.amadeus.com/TCTMIQ_15_1_1A')
        return response_data

    def void_tickets(self, message_id: str, ticket_numbers: List[str]):
        """
        Cancel documents by ticket numbers
        :param message_id: str -> the message id
        :param ticket_numbers: List[str] -> List of ticket numbers
        :return:
        """
        session_id, sequence_number, security_token = self.get_or_create_session_details(message_id)
        if security_token is None:
            raise NoSessionError(message_id)
        session_info = SessionInfo(security_token, sequence_number, session_id, message_id, False)
        request_data = self.xml_builder.void_tickets(session_info, ticket_numbers)
        response_data = self.__request_wrapper("void_tickets", request_data,
                                               'http://webservices.amadeus.com/TRCANQ_11_1_1A')

        return VoidTicketExtractor(response_data).extract()

    def cancel_pnr(self, message_id: str, close_session: bool = False):
        """
        Cancel the entire PNR
        :param message_id: str -> the message id
        :param close_session: bool -> Close or not the session
        :return:
        """
        session_id, sequence_number, security_token = self.get_or_create_session_details(message_id)
        session_info = SessionInfo(security_token, sequence_number, session_id, message_id, False)
        request_data = self.xml_builder.cancel_pnr(session_info, close_session)
        response_data = self.__request_wrapper("cancel_pnr", request_data,
                                               'http://webservices.amadeus.com/PNRXCL_17_1_1A')
        print(response_data)
        return CancelPnrExtractor(response_data).extract()
