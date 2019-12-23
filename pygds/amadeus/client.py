# coding: utf-8 client
from .xmlbuilders.builder import AmadeusXMLBuilder
from .errors import ClientError, ServerError
from pygds.core.payment import FormOfPayment
from typing import List
from pygds.amadeus.xml_parsers.retrive_pnr_v_fnc import GetPnrResponseExtractor
from pygds.core import generate_token
from pygds.core.price import StoreSegmentSelect, TSTInfo
from pygds.core.sessions import SessionInfo
from pygds.core.types import TravellerNumbering, Itinerary, Recommandation, ReservationInfo
from pygds.core.request import LowFareSearchRequest
from pygds.amadeus.xml_parsers.search_price_extract import PricePNRExtractor
from pygds.errors.gdserrors import NoSessionError
from pygds.core.client import BaseClient
from pygds.amadeus.xml_parsers.create_tst_extractor import CreateTstResponseExtractor, DisplayTSTExtractor
from pygds.amadeus.xml_parsers.response_extractor import PriceSearchExtractor, ErrorExtractor, SessionExtractor, \
    CommandReplyExtractor, \
    IssueTicketResponseExtractor, CancelPnrExtractor, QueueExtractor, InformativePricingWithoutPnrExtractor, \
    VoidTicketExtractor, UpdatePassengers, InformativeBestPricingWithoutPNRExtractor, SellFromRecommendationReplyExtractor, \
    FoPExtractor, RebookExtractor


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

    def open_session(self):
        """
            This method starts a new session to Amadeus.
        """
        request_data = self.xml_builder.start_transaction(None, self.office_id, self.username, self.password, None,
                                                          None)
        response_data = self.__request_wrapper("start_new_session", request_data,
                                               'http://webservices.amadeus.com/VLSSLQ_06_1_1A')

        return SessionExtractor(response_data).extract()

    def close_session(self, token: str):
        """
        This is for ending a current session
        :param message_id: the message id associated to that session
        :return: A GdsResponse containing the session info
        """
        message_id, session_id, sequence_number, security_token = self.decode_token(token)
        if not security_token:
            raise NoSessionError(message_id)
        request_data = self.xml_builder.end_session(message_id, session_id, sequence_number, security_token)
        response_data = self.__request_wrapper("end_new_session", request_data,
                                               'http://webservices.amadeus.com/VLSSOQ_04_1_1A')
        return SessionExtractor(response_data).extract()

    def decode_token(self, token: str):
        """
        This method is use to decode a token
        :param token: the token that we will decode
        :return message_id, session_id, sequence, security_token

        """
        payload = generate_token.decode_token(token)
        if not payload:
            return None, None, None, None
        else:
            values = payload["info_token"]
            return values["message_id"], values["session_id"], int(values["sequence"]) + 1, values["security_token"]

    def get_reservation(self, token: str, close_trx: bool, record_locator: str):
        """
            Return the reservation data from PNR.
        """
        message_id, session_id, sequence_number, security_token = self.decode_token(token)
        self.log.info(f"Retreive pnr '{record_locator}'.")
        request_data = self.xml_builder.get_reservation_builder(message_id, session_id, sequence_number, security_token, record_locator, close_trx)
        if security_token is None:
            self.log.warning("A new session will be created when retrieve pnr.")
        data = self.__request_wrapper("get_reservation", request_data, 'http://webservices.amadeus.com/PNRRET_17_1_1A')
        return GetPnrResponseExtractor(data).extract()

    def add_form_of_payment(self, token: str, fop: FormOfPayment, segment_refs: List[str], pax_refs: List[str], inf_refs: List[str], fop_sequence_number: str):
        """
            This method adds a form of payment to a PNR.
            The session must exists and a current PNR defined.
        """
        message_id, session_id, sequence_number, security_token = self.decode_token(token)
        if not security_token:
            raise NoSessionError(message_id)
        request_data = self.xml_builder.add_form_of_payment_builder(
            message_id, session_id, sequence_number, security_token, fop, segment_refs, pax_refs, inf_refs, fop_sequence_number)

        response_data = self.__request_wrapper("add_form_of_payment", request_data,
                                               'http://webservices.amadeus.com/TFOPCQ_15_4_1A')

        return FoPExtractor(response_data).extract()

    def pnr_add_multi_element(self, token, option_code, segment_name):
        """
            This method modifies the elements of a PNR (passengers, etc.)
        """
        message_id, session_id, sequence_number, security_token = self.decode_token(token)
        if not security_token:
            raise NoSessionError(message_id)
        request_data = self.xml_builder.pnr_add_multi_element_builder(session_id, sequence_number, security_token,
                                                                      message_id, option_code, segment_name)
        response_data = self.__request_wrapper("pnr_add_multi_element", request_data,
                                               'http://webservices.amadeus.com/PNRADD_17_1_1A')
        return GetPnrResponseExtractor(response_data).extract()

    def pnr_add_multi_for_pax_info_element(self, token, email_content, passenger_id, office_id):
        """
            This method modifies the elements of a PNR (passengers, etc.)
        """
        message_id, session_id, sequence_number, security_token = self.decode_token(token)
        if not security_token:
            raise NoSessionError(token)
        request_data = self.xml_builder.pnr_add_multi_element_for_pax_info_builder(session_id, sequence_number, security_token,
                                                                                   message_id, email_content, passenger_id, office_id)
        response_data = self.__request_wrapper("pnr_add_multi_for_pax_info_element", request_data,
                                               'http://webservices.amadeus.com/PNRADD_17_1_1A')
        return UpdatePassengers(response_data).extract()

    def cancel_list_segment(self, token, close_session: bool = False, segments: List[str] = []):
        """
            This method delete all segments
        """
        message_id, session_id, sequence_number, security_token = self.decode_token(token)
        if not security_token:
            raise NoSessionError(token)
        request_data = self.xml_builder.cancel_segments(session_id, sequence_number, security_token,
                                                        message_id, segments)
        response_data = self.__request_wrapper("cancel segments", request_data,
                                               'http://webservices.amadeus.com/PNRXCL_14_2_1A')
        return CancelPnrExtractor(response_data).extract()

    def cancel_information_passenger(self, reference, token):
        """
            This method modifies the elements of a PNR (passengers, etc.)
        """
        message_id, session_id, sequence_number, security_token = self.decode_token(token)
        if not security_token:
            raise NoSessionError(token)
        request_data = self.xml_builder.cancel_information_passenger(session_id, sequence_number, security_token,
                                                                     message_id, reference)
        response_data = self.__request_wrapper("cancel information passenger", request_data,
                                               'http://webservices.amadeus.com/PNRXCL_14_2_1A')
        return SessionExtractor(response_data).extract()

    def ticketing_pnr(self, token, passenger_reference_type, passenger_reference_value):
        """
            PNR ticketing process.
        """
        message_id, session_id, sequence_number, security_token = self.decode_token(token)
        if not security_token:
            raise NoSessionError(token)
        request_data = self.xml_builder.ticket_pnr_builder(message_id, session_id, sequence_number, security_token,
                                                           passenger_reference_type, passenger_reference_value)
        response_data = self.__request_wrapper("ticketing_pnr", request_data,
                                               'http://webservices.amadeus.com/TTKTIQ_15_1_1A')
        return IssueTicketResponseExtractor(response_data).extract()

    def issue_ticket_with_retrieve(self, token, tst_refs: List[str], pax_refs: List[str]):
        message_id, session_id, sequence_number, security_token = self.decode_token(token)
        if not session_id:
            raise NoSessionError(token)
        request_data = self.xml_builder.issue_ticket_retrieve(message_id, security_token, sequence_number, session_id,
                                                              tst_refs)
        response_data = self.__request_wrapper("issue_ticket_with_retrieve", request_data,
                                               'http://webservices.amadeus.com/TTKTIQ_15_1_1A')
        return IssueTicketResponseExtractor(response_data).extract()

    def fare_master_pricer_travel_board_search(self, low_fare_search: LowFareSearchRequest):
        """
            A method for searching prices of an itinerary.
        """
        request_data = self.xml_builder.fare_master_pricer_travel_board_search(self.office_id, low_fare_search)

        response_data = self.__request_wrapper("fare_master_pricer_travel_board_search", request_data,
                                               'http://webservices.amadeus.com/FMPTBQ_18_1_1A')

        return PriceSearchExtractor(response_data).extract()

    def fare_informative_price_without_pnr(self, numbering: TravellerNumbering, itineraries: List[Itinerary]):

        request_data = self.xml_builder.fare_informative_price_without_pnr(numbering, itineraries)
        response_data = self.__request_wrapper("fare_informative_price_without_pnr", request_data,
                                               'http://webservices.amadeus.com/TIPNRQ_18_1_1A')

        return InformativePricingWithoutPnrExtractor(response_data).extract()

    def fare_informative_best_pricing_without_pnr(self, recommandation: Recommandation):

        request_data = self.xml_builder.fare_informative_best_price_without_pnr(recommandation)
        response_data = self.__request_wrapper("fare_informative_best_price_without_pnr", request_data,
                                               'http://webservices.amadeus.com/TIBNRQ_18_1_1A')
        return InformativeBestPricingWithoutPNRExtractor(response_data).extract()

    def fare_check_rules(self, token: str, line_number):
        message_id, session_id, sequence_number, security_token = self.decode_token(token)
        if security_token is None:
            raise NoSessionError(message_id)
        request_data = self.xml_builder.fare_check_rules(message_id, session_id, sequence_number, security_token, line_number)
        response_data = self.__request_wrapper("check fare rules", request_data,
                                               'http://webservices.amadeus.com/FARQNQ_07_1_1A')
        return SessionExtractor(response_data).extract()

    def get_fare_rules(self, ticketing_date, rate_class, company_id, origin, destination):

        request_data = self.xml_builder.get_fare_rules(ticketing_date, rate_class, company_id, origin, destination)
        response_data = self.__request_wrapper("get fare rules", request_data,
                                               'http://webservices.amadeus.com/FARRNQ_10_1_1A')

        return SessionExtractor(response_data).extract()

    def sell_from_recommandation(self, itineraries: List[Itinerary]):
        request_data = self.xml_builder.sell_from_recomendation(itineraries)
        response_data = self.__request_wrapper("sell_from_recommandation", request_data,
                                               'http://webservices.amadeus.com/ITAREQ_05_2_IA')

        return SellFromRecommendationReplyExtractor(response_data).extract()

    def search_price_quote(self, token: str,
                           fare_type: str,
                           segment_select: list = [],
                           passengers: list = [],
                           baggage: int = 0,
                           region_name: str = ""):
        """
        Price a PNR with a booking class.
        The PNR is supposed to be supplied in the session on a previous call.
        :param message_id: The message id associated to
        :param price_request:
        :return:
        """
        message_id, session_id, sequence_number, security_token = self.decode_token(token)
        if security_token is None:
            raise NoSessionError(message_id)
        request_data = self.xml_builder.fare_price_pnr_with_booking_class(message_id, session_id,
                                                                          sequence_number,
                                                                          security_token,
                                                                          fare_type, passengers,
                                                                          segment_select)
        response_data = self.__request_wrapper("fare_price_pnr_with_booking_class", request_data,
                                               'http://webservices.amadeus.com/TPCBRQ_18_1_1A')
        return PricePNRExtractor(response_data).extract()

    def store_price_quote(self, token: str, fare_type: str, segment_select: List[StoreSegmentSelect],
                          passengers: dict = {}, baggage: int = 0, region_name: str = "", tst_info: TSTInfo = None):
        """
            Creates a TST from TST reference
            token: str
            tst_infos: List[TSTInfo]
        """

        message_id, session_id, sequence_number, security_token = self.decode_token(token)
        if security_token is None:
            raise NoSessionError(message_id)
        request_data = self.xml_builder.ticket_create_tst_from_price(message_id, session_id, sequence_number,
                                                                     security_token, tst_info)
        response_data = self.__request_wrapper("ticket_create_TST_from_pricing", request_data,
                                               'http://webservices.amadeus.com/TAUTCQ_04_1_1A')

        response_json = CreateTstResponseExtractor(response_data).extract()

        if response_json.application_error is not None:
            return response_json
        if response_json.session_info.security_token is None:
            return response_data

        return self.display_tst(
            response_json.session_info.security_token, response_json.payload
        )

    def display_tst(self, token: str, tst_info: TSTInfo):
        """
            Display a TST info
        """
        message_id, session_id, sequence_number, security_token = self.decode_token(token)
        if security_token is None:
            raise NoSessionError(message_id)
        request_data = self.xml_builder.display_tst(message_id, session_id, sequence_number,
                                                    security_token, tst_info)
        response_data = self.__request_wrapper("Display a tst info", request_data,
                                               'http://webservices.amadeus.com/TTSTRQ_13_2_1A')
        return DisplayTSTExtractor(response_data).extract()

    def re_book_air_segment(self, token: str, flight_segments: List[dict], pnr: str):
        """
            Add new Segment in the pnr
        """
        message_id, session_id, sequence_number, security_token = self.decode_token(token)
        if security_token is None:
            raise NoSessionError(message_id)
        request_data = self.xml_builder.re_book_air_segment(message_id, session_id, sequence_number,
                                                            security_token, flight_segments)
        response_data = self.__request_wrapper("air_rebook_air_segment", request_data,
                                               'http://webservices.amadeus.com/ARBKUR_14_1_1A')
        return RebookExtractor(response_data).extract()

    def create_pnr(self, token):
        """
            create the PNR
        """
        message_id, session_id, sequence_number, security_token = self.decode_token(token)
        if security_token is None:
            raise NoSessionError(message_id)
        request_data = self.xml_builder.create_pnr(message_id, session_id, sequence_number,
                                                   security_token)
        response_data = self.__request_wrapper("add_passenger_info", request_data,
                                               'http://webservices.amadeus.com/PNRADD_17_1_1A')
        return GetPnrResponseExtractor(response_data).extract()

    def send_command(self, command: str, token: str = None, close_trx: bool = False):
        """
        Send a command to Amadeus API
        :param command: the command to send as str
        :param message_id: The message id as str. Can be None if starting a new session
        :param close_trx: boolean telling if we are ending or not the current session
        :return: GdsResponse with the response of the command as payload
        """
        message_id, session_id, sequence_number, security_token = self.decode_token(token)
        self.log.info(f"Sending command '{command}' to Amadeus server.")
        request_data = self.xml_builder.send_command(command, message_id, session_id, sequence_number, security_token,
                                                     close_trx)
        if security_token is None:
            self.log.warning("A new session will be created when sending the command.")
        data = self.__request_wrapper("send_command", request_data, 'http://webservices.amadeus.com/HSFREQ_07_3_1A')
        return CommandReplyExtractor(data).extract()

    def delete_all_price_quotes(self, token):
        return self.send_command(token, "TTE/ALL")

    def transfer_profile(self, token: str):
        pass

    def add_fare_type_remark(self, token: str, fare_type: str, passenger_type: str):
        pass

    def send_remark(self, token: str, close_trx: bool, remark_text: str, remark_type: str = "General"):
        pass

    def add_passenger_info(self, token: str, reservation_infos: ReservationInfo):
        """
            add passenger info and create the PNR
        """
        message_id, session_id, sequence_number, security_token = self.decode_token(token)
        if security_token is None:
            raise NoSessionError(message_id)
        request_data = self.xml_builder.add_passenger_info(self.office_id, message_id, session_id, sequence_number,
                                                           security_token, reservation_infos)
        response_data = self.__request_wrapper("add_passenger_info", request_data,
                                               'http://webservices.amadeus.com/PNRADD_17_1_1A')

        return GetPnrResponseExtractor(response_data).extract()

    def add_office_id(self, token: str, office_id: str):
        """
            add passenger info and create the PNR
        """
        message_id, session_id, sequence_number, security_token = self.decode_token(token)
        if security_token is None:
            raise NoSessionError(message_id)
        request_data = self.xml_builder.add_office_id(office_id, message_id, session_id, sequence_number,
                                                      security_token)
        response_data = self.__request_wrapper("add_office_id", request_data,
                                               'http://webservices.amadeus.com/PNRADD_17_1_1A')

        return GetPnrResponseExtractor(response_data).extract()

    def pnr_add_ssr(self, token: str, passenger_ids: str, content: str, company_id: str):
        """
            add passenger info and create the PNR
        """
        message_id, session_id, sequence_number, security_token = self.decode_token(token)
        if security_token is None:
            raise NoSessionError(message_id)
        request_data = self.xml_builder.pnr_add_ssr(session_id, sequence_number,
                                                    security_token, message_id, passenger_ids, content, company_id)
        response_data = self.__request_wrapper("add_ssr_in_pnr", request_data,
                                               'http://webservices.amadeus.com/PNRADD_17_1_1A')

        return GetPnrResponseExtractor(response_data).extract()

    def queue_place_pnr(self, token: str, pnr: str, queues: List[str]):

        message_id, session_id, sequence_number, security_token = self.decode_token(token)
        if security_token is None:
            raise NoSessionError(message_id)
        request_data = self.xml_builder.queue_place_pnr(message_id, session_id, sequence_number, security_token, pnr,
                                                        queues)
        response_data = self.__request_wrapper("queue_place_pnr", request_data, 'http://webservices.amadeus.com/QUQPCQ_03_1_1A')

        return QueueExtractor(response_data).extract()

    def issue_combined(self, token: str, passengers: List[str], segments: List[str], retrieve_pnr: bool):
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
        message_id, session_id, sequence_number, security_token = self.decode_token(token)
        if security_token is None:
            raise NoSessionError(message_id)
        session_info = SessionInfo(security_token, sequence_number, session_id, message_id, False)
        request_data = self.xml_builder.issue_combined(session_info, passengers, segments, retrieve_pnr)
        response_data = self.__request_wrapper("issue_combined", request_data,
                                               'http://webservices.amadeus.com/TCTMIQ_15_1_1A')
        return SessionExtractor(response_data).extract()

    def create_tsm(self, token: str, passenger_id: str, tsm_type: str):
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
        message_id, session_id, sequence_number, security_token = self.decode_token(token)

        if security_token is None:
            raise NoSessionError(message_id)

        session_info = SessionInfo(security_token, sequence_number, session_id, message_id, False)
        request_data = self.xml_builder.create_tsm(session_info, passenger_id, tsm_type)
        response_data = self.__request_wrapper("create tsm", request_data,
                                               'http://webservices.amadeus.com/TMCOCQ_07_3_1A')
        return IssueTicketResponseExtractor(response_data).extract()

    def void_tickets(self, token: str, ticket_numbers: List[str]):
        """
        Cancel documents by ticket numbers
        :param message_id: str -> the message id
        :param ticket_numbers: List[str] -> List of ticket numbers
        :return:
        """

        message_id, session_id, sequence_number, security_token = self.decode_token(token)
        if security_token is None:
            raise NoSessionError(message_id)
        session_info = SessionInfo(security_token, sequence_number, session_id, message_id, False)
        request_data = self.xml_builder.void_tickets(session_info, ticket_numbers)
        response_data = self.__request_wrapper("void_tickets", request_data,
                                               'http://webservices.amadeus.com/TRCANQ_11_1_1A')

        return VoidTicketExtractor(response_data).extract()

    def cancel_pnr(self, token: str, close_session: bool = False):
        """
        Cancel the entire PNR
        :param message_id: str -> the message id
        :param close_session: bool -> Close or not the session
        :return:
        """
        message_id, session_id, sequence_number, security_token = self.decode_token(token)
        session_info = SessionInfo(security_token, sequence_number, session_id, message_id, False)
        request_data = self.xml_builder.cancel_pnr(session_info, close_session)
        response_data = self.__request_wrapper("cancel_pnr", request_data,
                                               'http://webservices.amadeus.com/PNRXCL_17_1_1A')
        return CancelPnrExtractor(response_data).extract()
