# This file will be change for refactoring purpose.
# This file is for Sabre reservation classes and functions
# TODO: Use "import" statements for packages and modules only, not for individual classes or functions.
# Note that there is an explicit exemption for
import json
from typing import List

import requests
import deprecation
from datetime import datetime

from pygds.amadeus.errors import ServerError, ClientError
from pygds.core.payment import FormOfPayment
from pygds.sabre.json_parsers.new_rest_token_extractor import extract_sabre_rest_token
from pygds.sabre.json_parsers.response_extractor import CreatePnrExtractor, AircraftExtractor
from pygds.sabre.json_parsers.revalidate_extract import RevalidateItineraryExtractor
from pygds.sabre.jsonbuilders.builder import SabreJSONBuilder
from pygds.core.request import LowFareSearchRequest
from pygds.core.security_utils import generate_random_message_id
from pygds.core.helpers import get_data_from_xml
from pygds.core.price import StoreSegmentSelect
from pygds.sabre.xml_parsers.response_extractor import PriceSearchExtractor, DisplayPnrExtractor, SendCommandExtractor, \
    IssueTicketExtractor, EndTransactionExtractor, \
    SendRemarkExtractor, SabreQueuePlaceExtractor, SabreIgnoreTransactionExtractor, SeatMapResponseExtractor, \
    IsTicketExchangeableExtractor, ExchangeShoppingExtractor, \
    ExchangePriceExtractor, ExchangeCommitExtractor, UpdatePassengerExtractor, RebookExtractor, CloseSessionExtractor, \
    SabreSoapErrorExtractor, CancelSegmentExtractor, SingleVoidExtractor
from pygds.core.client import BaseClient, session_wrapper, RestToken
from pygds.core.sessions import SessionInfo, TokenType
from pygds.sabre.xml_parsers.sessions import SessionExtractor
from pygds.sabre.xmlbuilders.builder import SabreXMLBuilder
from pygds.core.types import PassengerUpdate, FlightSeatMap, Passenger
from pygds.sabre.jsonbuilders.rest_token_builder import build_sabre_new_rest_token_header


class SabreClient(BaseClient):
    """
    A class to interact with Sabre GDS
    """

    def __init__(self, endpoint: str, rest_url, username: str, password: str, pcc: str, debug: bool = False):
        super().__init__(endpoint, username, password, pcc, debug)
        self.xml_builder = SabreXMLBuilder(endpoint, username, password, pcc)
        self.json_builder = SabreJSONBuilder("Production")
        self.rest_url = rest_url
        self.header_template = {'content-type': 'text/xml; charset=utf-8'}
        self.rest_header = {
            'Authorization': "Bearer",
            'Content-Type': 'application/json; charset=utf-8'
        }
        self._current_rest_token: RestToken = None

    def _rest_request_wrapper(self, request_data, url_path, token):
        """
            This wrapper method helps wrap request with
        """
        headers = self.rest_header
        headers["Authorization"] = "Bearer " + token
        response = requests.post(self.rest_url + url_path, data=request_data, headers=headers)

        if self.is_debugging:
            status = response.status_code
            self.log.debug(request_data)
            self.log.debug(response.content)
            self.log.debug(f"{url_path} status: {status}")
        return response

    def _soap_request_wrapper(self, request_data):
        """
            This  wrapper method helps wrap request
        """
        headers = self.header_template
        return requests.post(self.endpoint, data=request_data, headers=headers)

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
            error = SabreSoapErrorExtractor(response.content).extract()
            sess, (faultcode, faultstring) = error.session_info, error.payload
            self.log.error(f"faultcode: {faultcode}, faultstring: {faultstring}")
            raise ServerError(sess, status, faultcode, faultstring)
        elif status == 400:
            sess = SessionExtractor(response.content).extract()
            raise ClientError(sess, status, "Client Error")
        return response.content

    def open_session(self):
        """
        This will open a new session
        :return: a token session
        """
        message_id = generate_random_message_id()
        open_session_xml = self.xml_builder.session_create_rq(message_id)
        response = self.__request_wrapper("open_session", open_session_xml, "SessionCreateRQ")
        gds_response = SessionExtractor(response).extract()
        return gds_response.session_info.security_token

    def close_session(self, token: str):
        """
        A method to close a session
        :param token: the  token
        :return: True if session closed else None
        """
        close_session_request = self.xml_builder.session_close_rq(token)
        close_session_response = self.__request_wrapper("close_session", close_session_request, self.endpoint)
        self.log.info(f"Close_session: Session associated to the token {token} is closed")
        return CloseSessionExtractor(close_session_response).extract().payload

    @session_wrapper
    def get_reservation(self, token: str, pnr: str, current: bool = False):
        """retrieve PNR
        :param pnr: the record locator
        :param token: the message identifier
        :return: a Reservation object
        """
        display_pnr_request = self.xml_builder.get_reservation_rq(token, pnr)
        display_pnr_response = self.__request_wrapper("get_reservation", display_pnr_request, self.xml_builder.url)
        gds_response = DisplayPnrExtractor(display_pnr_response).extract()
        return gds_response

    @session_wrapper
    def search_price_quote(self, token: str, fare_type: str = '', segment_select: list = [],
                           passenger_type: list = [], baggage: int = 0, region_name: str = ""):
        """
        A method to search price
        :param token: the token
        :param fare_type: the fare type value value
        :param segment_select: the list of segment selected
        :param  passenger_type: the list of passenger type selected
        :param baggage: number of baggage
        :param region_name: the region name
        :return:
        """
        search_price_request = self.xml_builder.price_quote_rq(token, retain=False, fare_type=fare_type,
                                                               segment_select=segment_select,
                                                               passenger_type=passenger_type, baggage=baggage,
                                                               region_name=region_name)
        search_price_response = self.__request_wrapper("search_price_quote", search_price_request, self.endpoint)
        response = PriceSearchExtractor(search_price_response).extract()
        return response

    def store_price_quote(self, token: str, segment_select: List[StoreSegmentSelect],
                          passenger: dict = {}, baggage: int = 0, region_name: str = "", tst_info=None):
        """
        A method to store price
        :param token: the token
        :param fare_type: the fare type value value
        :param segment_select: the list of segment selected
        :param passengers: dict
        :param baggage: number of baggage
        :param region_name: the region name
        :return:
        """
        # if segment select is not given as couple of (segment number, brand id) we will
        # will rewrite it with null brand id to fit the request builder requirements
        fare_type = "Net" if str(passenger["code"]).startswith("J") else "Pub"
        corrected_segments: List[StoreSegmentSelect] = []
        for s in segment_select:
            if not isinstance(s, tuple):
                s = (s, None)
            corrected_segments.append(s)
        store_price_request = self.xml_builder.store_price_rq(token, fare_type=fare_type,
                                                              segment_select=corrected_segments,
                                                              passenger_type=passenger,
                                                              region_name=region_name)
        self.log.debug(f"Baggage {baggage} is given but not used in construction of request.")
        store_price_response = self.__request_wrapper("store_price_quote", store_price_request, self.endpoint)
        response = PriceSearchExtractor(store_price_response).extract()
        session_info = SessionInfo(token, 1, None, None, False, TokenType.SESSION_TOKEN)
        session_info.last_access = datetime.now()
        response.session_info = session_info
        return response

    @session_wrapper
    def cancel_list_segment(self, token: str, list_segment):
        """
        A method to cancel segment
        :param token: the token session
        :param list_segment: the list of segment selected
        """
        cancel_segment_request = self.xml_builder.cancel_segment_rq(token, list_segment)
        cancel_segment_response = self.__request_wrapper("cancel_list_segment", cancel_segment_request, self.endpoint)
        response = CancelSegmentExtractor(cancel_segment_response).extract()
        return response

    def search_flight(self, search_request: LowFareSearchRequest, available_only: bool, types: str):
        """
        This function is for searching flight
        :param search_request:
        :param available_only:
        :param types:
        :return:
        :return : available flight for the specific request_search
        """
        token = self.get_rest_token()
        search_flight_request = self.json_builder.search_flight_builder(search_request, available_only, types)
        search_response = self._rest_request_wrapper(json.dumps(search_flight_request),
                                                     "/v4.1.0/shop/flights?mode=live", token)
        return search_response.content

    @deprecation.deprecated(deprecated_in="0.0.9", details="Use the get_rest_token function instead")
    def new_rest_token(self):
        """
        This will open a new session
        :return: a Session token
        """
        message_id = generate_random_message_id()
        open_session_xml = self.xml_builder.session_token_rq()
        response = self._request_wrapper(open_session_xml, None)
        token = get_data_from_xml(response.content, "soap-env:Envelope", "soap-env:Header", "wsse:Security",
                                  "wsse:BinarySecurityToken")["#text"]
        session_info = SessionInfo(token, 1, message_id, token, False, TokenType.REST_TOKEN)
        self.add_session(session_info)
        return session_info

    def get_rest_token(self) -> str:
        """
        This method will get a rest Token, by calling Sabre if necessary
        :return:
        """
        token_object = self._current_rest_token
        if not token_object or token_object.is_expired():
            self.log.debug(f"PCC {self.office_id}: No REST token or expired")
            token_object = self._generate_new_rest_token()
            self._current_rest_token = token_object
        return token_object.token

    def _generate_new_rest_token(self) -> RestToken:
        self.log.debug(f"calling Sabre to get new REST token for PCC {self.office_id}")
        headers = {
            'Authorization': f"Basic {build_sabre_new_rest_token_header(self.office_id, self.username, self.password)}",
            'Accept': '*/*'
        }
        request_data = {"grant_type": "client_credentials"}
        response = requests.post(f"{self.rest_url}/v2/auth/token", headers=headers, data=request_data)
        if response.status_code == requests.codes.ok:
            return extract_sabre_rest_token(response.text)
        return RestToken(None, None)

    @session_wrapper
    def issue_ticket(self, token: str, price_quote, form_of_payment: FormOfPayment, fare_type=None,
                     commission_percentage=None, markup=None, name_select=None):
        """
        This function is make for the ticket process.
        she does not want to make the end transaction at the end to commit the change
        :return
        """
        air_ticket_request = self.xml_builder.air_ticket_rq(token, price_quote, form_of_payment, fare_type,
                                                            commission_percentage, markup, name_select)
        air_ticket_response = self.__request_wrapper("issue_ticket", air_ticket_request, self.endpoint)
        gds_response = IssueTicketExtractor(air_ticket_response).extract()
        return gds_response

    def end_transaction(self, token: str, close_session: bool = True):
        """
        This function is for end transaction
        """
        request_data = self.xml_builder.end_transaction_rq(token)
        response_data = self.__request_wrapper("end_transaction", request_data, self.endpoint)
        gds_response = EndTransactionExtractor(response_data).extract()
        if close_session is True:
            self.close_session(token)
        return gds_response

    @session_wrapper
    def send_remark(self, token: str, remark_text, remark_type: str = "General"):
        """this will send a remark for a pnr
        :param token: the security token
        :param remark_text: the remark text
        :param remark_type: the remark type
        :return dict:
        """
        request = self.xml_builder.send_remark_rq(token, remark_text, remark_type)
        send_remark_request = request.encode(encoding='UTF-8')
        send_remark_response = self.__request_wrapper("send_remark", send_remark_request, self.endpoint)
        response = SendRemarkExtractor(send_remark_response).extract()
        return response

    @session_wrapper
    def re_book_air_segment(self, token: str, flight_segment, pnr):
        """
        A method to rebook air segment
        :param token: the security token
        :param flight_segment: list of flight segment
        :param pnr: the pnr
        :return:
        """
        re_book_air_segment_request = self.xml_builder.re_book_air_segment_rq(token, flight_segment, pnr)
        re_book_air_segment_response = self.__request_wrapper("re_book_air_segment", re_book_air_segment_request,
                                                              self.endpoint)
        response = RebookExtractor(re_book_air_segment_response).extract()
        return response

    @session_wrapper
    def send_command(self, token: str, command: str):
        """send command
        :param token: the security token
        :param command: the value of the command
        """
        request = self.xml_builder.sabre_command_lls_rq(token, command)
        command_request = request.encode(encoding='UTF-8')
        command_response = self.__request_wrapper("send_command", command_request, self.endpoint)
        gds_response = SendCommandExtractor(command_response).extract()
        return gds_response

    def delete_all_price_quotes(self, token):
        return self.send_command(token, close_session=False, command="PQD-ALL")

    def transfer_profile(self, token):
        self.send_command(token, False, "CC/PC")

    def add_fare_type_remark(self, token: str, passenger_type: str):
        fare_type = "Net" if str(passenger_type.startswith("J")) else "Pub"
        ud_fare_type = "N" if fare_type == "Net" else "P"
        self.send_command(token, False, f"5.S*UD25 {ud_fare_type}")  # Ajouter remark

    def add_username_remark(self, token: str, username: str):
        self.send_command(token, False, "5.S*UD100 " + str(username))

    def portal_remark(self, token: str):
        self.send_command(token, False, "6PORTAL")

    @session_wrapper
    def queue_place(self, token: str, queue_number: str, record_locator: str):
        """This function is for queue place
        """
        request_data = self.xml_builder.queue_place_rq(token, queue_number, record_locator)
        response_data = self.__request_wrapper("queue place", request_data, self.endpoint)
        gds_response = SabreQueuePlaceExtractor(response_data).extract()
        return gds_response

    @session_wrapper
    def ignore_transaction(self, token: str):
        """
        This function is for ignore transaction
        """
        request_data = self.xml_builder.ignore_transaction_rq(token)
        response_data = self.__request_wrapper("ignore transaction", request_data, self.endpoint)
        gds_response = SabreIgnoreTransactionExtractor(response_data).extract()
        return gds_response

    @session_wrapper
    def is_ticket_exchangeable(self, token: str, ticket_number: str):
        """ A method to check if the ticket number is exchangeable

        Arguments:
            token {str} -- The security token
            ticket_number {str} -- The ticket number

        Returns:
            [IsTicketExchangeableExtractor] -- Ticket Exchangeable Extractor
        """
        electronic_document_request = self.xml_builder.electronic_document_rq(token, ticket_number)
        electronic_document_response = self.__request_wrapper(
            "is_ticket_exchangeable",
            electronic_document_request,
            self.endpoint)
        gds_response = IsTicketExchangeableExtractor(electronic_document_response).extract()
        return gds_response

    @session_wrapper
    def exchange_shopping(self, token: str, pnr: str, passengers: List[dict], origin_destination: List[dict]):
        """A method to search for applicable itinerary reissue options for an existing ticket

        Arguments:
            token {str} -- the security token
            pnr {str} -- the pnr code

        Keyword Arguments:
            passengers {list} -- list of passengers information (default: {[dict]})
            origin_destination {list} -- list of itineraries information (default: {[dict]})

        Returns:
            [ExchangeShoppingExtractor] -- [description]
        """
        exchange_shopping_request = self.xml_builder.exchange_shopping_rq(
            token,
            pnr,
            passengers,
            origin_destination
        )

        exchange_shopping_response = self.__request_wrapper(
            "exchange_shopping",
            exchange_shopping_request,
            self.endpoint
        )
        gds_response = ExchangeShoppingExtractor(exchange_shopping_response).extract()
        return gds_response

    @session_wrapper
    def exchange_price(self, token: str, ticket_number: str, name_number: str, passenger_type: str):
        """
        A method to price an air ticket exchange
        :param token: the security token
        :param ticket_number: the ticket number
        :param name_number: the passenger name number
        :param passenger_type: the passenger type
        :return:
        """
        exchange_price_request = self.xml_builder.automated_exchanges_price_rq(token, ticket_number, name_number,
                                                                               passenger_type)
        exchange_price_response = self.__request_wrapper("exchange_price", exchange_price_request, self.endpoint)
        gds_response = ExchangePriceExtractor(exchange_price_response).extract()
        return gds_response

    @session_wrapper
    def exchange_commit(self, token: str, price_quote: int, form_of_payment: FormOfPayment, fare_type: str, commission_percent: str = None, markup: str = None):
        """A method to price an air ticket exchange

        Arguments:
            token {str} -- The security token
            price_quote {int} -- The pq number
            form_of_payment {FormOfPayment} -- The type of payment
            fare_type {str} -- The fare type

        Keyword Arguments:
            commission_percent {str} -- the value of commission (default: {None})
            markup {str} -- The value of markup (default: {None})

        Returns:
            [ExchangeCommitExtractor] -- Exchange Commit Extractor
        """

        exchange_commit_request = self.xml_builder.automated_exchanges_commmit_rq(
            token,
            price_quote,
            form_of_payment,
            fare_type,
            commission_percent,
            markup
        )
        exchange_commit_response = self.__request_wrapper("exchange_commit", exchange_commit_request, self.endpoint)
        gds_response = ExchangeCommitExtractor(exchange_commit_response).extract()
        return gds_response

    @session_wrapper
    def exchange_ticket(self, token: str, price_quote: int):
        """This method is make for the ticket process.
        she does not want to make the end transaction at the end to commit the change

        Arguments:
            token {str} -- The security token
            price_quote {int} -- Price quote number

        Returns:
            [IssueTicketExtractor] -- Issue Ticket Extractor
        """
        ticketing_exchange_request = self.xml_builder.ticketing_exchange_rq(token, price_quote)
        ticketing_exchange_response = self.__request_wrapper("exchange_ticket", ticketing_exchange_request, self.endpoint)
        gds_response = IssueTicketExtractor(ticketing_exchange_response).extract()
        return gds_response

    def create_pnr_rq(self, create_pnr_request):
        """
        the create pnr request builder
        Arguments:
            create_pnr_request {[CreatPnrRequest]} -- [the pnr request]
        Returns:
            [GdsResponse] -- [create pnr response ]
        """
        token = self.get_rest_token()
        request_data = self.json_builder.create_pnr_builder(create_pnr_request)
        response = self._rest_request_wrapper(request_data, "/v2.2.0/passenger/records?mode=create", token)
        gds_response = CreatePnrExtractor(response.content).extract()
        return gds_response

    @session_wrapper
    def seat_map(self, token: str, flight_request: FlightSeatMap, passenger_request: List[Passenger]):
        """[This function will return the result for the seat map request]

        Arguments:
            token {[str]} -- [the security token]
            flight_request {[FlightSeatMap]} -- [this will handler the flight request]
            passenger_request {[PassengerUpdate]} -- [this will handler the flight request]
        """
        seat_map_request = self.xml_builder.seap_map_rq(token, flight_request, passenger_request)
        seat_map_response = self.__request_wrapper("seat_map", seat_map_request, self.endpoint)
        gds_response = SeatMapResponseExtractor(seat_map_response).extract()
        return gds_response

    @session_wrapper
    def update_passenger(self, token: str, pnr: str, passenger_update: PassengerUpdate):
        """
        Arguments:
            token {str} -- [ the security token]
            pnr {str} -- [ the pnr code ]
            passenger_update {[PassengerUpdate]} -- [the element to update]
        """
        update_passenger_request = self.xml_builder.update_passenger_rq(token, pnr, passenger_update)
        update_passenger_response = self.__request_wrapper("update_passenger", update_passenger_request, self.endpoint)
        gds_response = UpdatePassengerExtractor(update_passenger_response).extract()
        return gds_response

    def revalidate_itinerary(self, itineraries: list = [], passengers: list = [],
                             fare_type: str = None, pseudo_city_code: str = None):
        """
        The Revalidate Itinerary (revalidate_itinerary) is used to recheck the availability and price of a
        specific itinerary option without booking the itinerary.
        The solution re-validates if the itinerary option is valid for purchase.
        Arguments:
            itineraries{list}: list itineraries
            passengers{list}: list passengers
            fare_type{str}: fare type(Net or Pub)
            pseudo_city_code{str} : The PCC
        Returns:
            [GdsResponse] -- [revalidate itinerary response]
        """
        token = self.get_rest_token()
        revalidate_request = self.json_builder.revalidate_build(pseudo_city_code, itineraries, passengers, fare_type)
        revalidate_response = self._rest_request_wrapper(revalidate_request, "/v4.3.0/shop/flights/revalidate", token)
        gds_response = RevalidateItineraryExtractor(revalidate_response.content).extract()
        return gds_response

    @session_wrapper
    def void_ticket(self, token: str, rph):
        """[A method to void a ticket number]

        Arguments:
            token {str} -- [the security token]]
            rph {[type]} -- [the ticket number identifier]

        Returns:
            [GdsResponse] -- [Single Void Response]
        """
        void_ticket_request = self.xml_builder.void_ticket_rq(token, rph)
        void_ticket_response = self.__request_wrapper("void_ticket", void_ticket_request, self.endpoint)
        gds_response = SingleVoidExtractor(void_ticket_response).extract()
        return gds_response

    def aircrafts(self):
        """[The Aircraft Equipment Lookup API returns the aircraft name associated with a specified IATA aircraft equipment code.]
        Returns:
            [list] -- [list of aircraft types]
        """
        token = self.get_rest_token()
        headers = self.rest_header
        headers["Authorization"] = "Bearer " + token
        response = requests.get(f"{self.rest_url}/v1/lists/utilities/aircraft/equipment", headers=headers)
        gds_response = AircraftExtractor(response.content).extract()
        return gds_response
