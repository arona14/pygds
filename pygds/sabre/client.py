# This file will be change for refactoring purpose.
# This file is for Sabre reservation classes and functions
# TODO: Use "import" statements for packages and modules only, not for individual classes or functions.
# Note that there is an explicit exemption for
import json
import requests

from pygds.amadeus.errors import ServerError, ClientError
from pygds.core.payment import FormOfPayment
from pygds.sabre.json_parsers.response_extractor import CreatePnrExtractor
from pygds.sabre.json_parsers.revalidate_extract import RevalidateItineraryExtractor
from pygds.sabre.jsonbuilders.builder import SabreJSONBuilder
from pygds.core.request import LowFareSearchRequest
from pygds.core.security_utils import generate_random_message_id
from pygds.core.helpers import get_data_from_xml
from pygds.sabre.xml_parsers.response_extractor import PriceSearchExtractor, DisplayPnrExtractor, SendCommandExtractor, IssueTicketExtractor, EndTransactionExtractor, \
    SendRemarkExtractor, SabreQueuePlaceExtractor, SabreIgnoreTransactionExtractor, SeatMapResponseExtractor, IsTicketExchangeableExtractor, ExchangeShoppingExtractor, \
    ExchangePriceExtractor, ExchangeCommitExtractor, UpdatePassengerExtractor, RebookExtractor, CloseSessionExtractor, SabreSoapErrorExtractor
from pygds.errors.gdserrors import NoSessionError
from pygds.core.client import BaseClient
from pygds.core.sessions import SessionInfo, TokenType
from pygds.sabre.xml_parsers.sessions import SessionExtractor
from pygds.sabre.xmlbuilders.builder import SabreXMLBuilder
from pygds.core.types import PassengerUpdate, FlightSeatMap


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

    def _rest_request_wrapper(self, request_data, url_path, token):
        """
            This wrapper method helps wrap request with
        """
        headers = self.rest_header
        headers["Authorization"] = "Bearer " + token
        return requests.post(self.rest_url + url_path, data=request_data, headers=headers)

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
        session_info = gds_response.session_info
        session_info.token_type = TokenType.SESSION_TOKEN
        self.add_session(session_info)
        return session_info

    def close_session(self, message_id, remove_session: bool = True):
        """
        A method to close a session
        :param message_id: the message id associated to the token
        :param remove_session: bool -> Tell if we will remove the session from holder
        :return: True if session closed else None
        """
        _, _, token = self.get_or_create_session_details(message_id)
        if token:
            close_session_request = self.xml_builder.session_close_rq(token)
            close_session_response = self.__request_wrapper("close_session", close_session_request, self.endpoint)
            self.log.info(f"Close_session: Session associated to message id {message_id} is closed")
            if remove_session:
                self.session_holder.remove_session(message_id)
            return CloseSessionExtractor(close_session_response).extract().payload

    def get_reservation(self, token: str, pnr: str):
        """retrieve PNR
        :param pnr: the record locator
        :param token: the message identifier
        :return: a Reservation object
        """
        display_pnr_request = self.xml_builder.get_reservation_rq(token, pnr)
        display_pnr_response = self.__request_wrapper("get_reservation", display_pnr_request, self.xml_builder.url)
        gds_response = DisplayPnrExtractor(display_pnr_response).extract()
        return gds_response

    def search_price_quote(self, message_id, retain: bool = False, fare_type: str = '', segment_select: list = [], passenger_type: list = [], baggage: int = 0, region_name: str = ""):
        """
        A method to search price
        :param message_id: the message id
        :param retain: the retain value
        :param fare_type: the fare type value value
        :param segment_select: the list of segment selected
        :param  passenger_type: the list of passenger type selected
        :param baggage: number of baggage
        :param region_name: the region name
        :return:
        """
        session_info = self.get_session_info(message_id)
        if session_info is None:
            raise NoSessionError(message_id)
        token_session = session_info.security_token
        search_price_request = self.xml_builder.price_quote_rq(token_session, retain=retain, fare_type=fare_type, segment_select=segment_select, passenger_type=passenger_type, baggage=baggage, region_name=region_name)
        search_price_response = self.__request_wrapper("search_price_quote", search_price_request, self.endpoint)
        session_info.increment_sequence()
        self.add_session(session_info)
        response = PriceSearchExtractor(search_price_response).extract()
        response.session_info = session_info
        return response

    def store_price_quote(self, message_id, retain: bool = True, fare_type: str = '', segment_select: list = [], passengers: dict = {}, baggage: int = 0, region_name: str = "", brand_id: str = None):
        """
        A method to store price
        :param message_id: the message id
        :param retain: the retain value
        :param fare_type: the fare type value value
        :param segment_select: the list of segment selected
        :param baggage: number of baggage
        :param region_name: the region name
        :param brand_id
        :return:
        """
        session_info = self.get_session_info(message_id)
        if session_info is None:
            raise NoSessionError(message_id)
        token_session = session_info.security_token
        store_price_request = self.xml_builder.price_quote_rq(token_session, retain=retain, fare_type=fare_type, segment_select=segment_select, passenger_type=passengers, baggage=baggage, region_name=region_name, brand_id=brand_id)
        store_price_response = self.__request_wrapper("store_price_quote", store_price_request, self.endpoint)
        session_info.increment_sequence()
        self.add_session(session_info)
        response = PriceSearchExtractor(store_price_response).extract()
        response.session_info = session_info
        return response

    def cancel_list_segment(self, token_session, list_segment):
        """
        A method to cancel segment
        :param token_session: the token session
        :param list_segment: the list of segment selected
        """
        return self.xml_builder.cancel_segment_rq(token_session, list_segment)

    def search_flight(self, message_id, search_request: LowFareSearchRequest, available_only: bool, types: str):
        """
        This function is for searching flight
        :return : available flight for the specific request_search
        """
        session_info = self.get_session_info(message_id)
        if not session_info:
            self.log.info(f"Sorry but we didn't find a token with {message_id}. Creating a new one.")
            session_info = self.new_rest_token()
        else:
            self.log.info("you already have a token! No need to create a new one for search flights")
        search_flight_request = self.json_builder.search_flight_builder(search_request, available_only, types)
        search_response = self._rest_request_wrapper(json.dumps(search_flight_request), "/v4.1.0/shop/flights?mode=live", session_info.security_token)
        self.add_session(session_info)
        return search_response.content

    def new_rest_token(self):
        """
        This will open a new session
        :return: a Session token
        """
        message_id = generate_random_message_id()
        open_session_xml = self.xml_builder.session_token_rq()
        response = self._request_wrapper(open_session_xml, None)
        token = get_data_from_xml(response.content, "soap-env:Envelope", "soap-env:Header", "wsse:Security", "wsse:BinarySecurityToken")["#text"]
        session_info = SessionInfo(token, 1, message_id, token, False, TokenType.REST_TOKEN)
        self.add_session(session_info)
        return session_info

    def issue_ticket(self, message_id, price_quote, form_of_payment: FormOfPayment, fare_type=None, commission_percentage=None, markup=None, name_select=None):
        """
        This function is make for the ticket process.
        she does not want to make the end transaction at the end to commit the change
        :return
        """
        session_info = self.get_session_info(message_id)
        if session_info is None:
            raise NoSessionError(message_id)
        token_session = session_info.security_token
        air_ticket_request = self.xml_builder.air_ticket_rq(token_session, price_quote, form_of_payment, fare_type, commission_percentage, markup, name_select)
        air_ticket_response = self.__request_wrapper("issue_ticket", air_ticket_request, self.endpoint)
        session_info.increment_sequence()
        self.add_session(session_info)
        gds_response = IssueTicketExtractor(air_ticket_response).extract()
        gds_response.session_info = session_info
        return gds_response

    def end_transaction(self, token: str):
        """
        This function is for end transaction
        """
        request_data = self.xml_builder.end_transaction_rq(token)
        response_data = self.__request_wrapper("end_transaction", request_data, self.endpoint)
        gds_response = EndTransactionExtractor(response_data).extract()
        return gds_response

    def send_remark(self, token: str, text):
        """this will send a remark for a pnr
        :param token: the security token
        :param text: the remark text
        :return:
        """
        request = self.xml_builder.send_remark_rq(token, text)
        send_remark_request = request.encode(encoding='UTF-8')
        send_remark_response = self.__request_wrapper("send_remark", send_remark_request, self.endpoint)
        response = SendRemarkExtractor(send_remark_response).extract()
        return response

    def re_book_air_segment(self, token: str, flight_segment, pnr):
        """
        A method to rebook air segment
        :param token: the security token
        :param flight_segment: list of flight segment
        :param pnr: the pnr
        :return:
        """
        re_book_air_segment_request = self.xml_builder.re_book_air_segment_rq(token, flight_segment, pnr)
        re_book_air_segment_response = self.__request_wrapper("re_book_air_segment", re_book_air_segment_request, self.endpoint)
        response = RebookExtractor(re_book_air_segment_response).extract()
        return response

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

    def queue_place(self, token: str, queue_number: str, record_locator: str):
        """This function is for queue place
        """
        request_data = self.xml_builder.queue_place_rq(token, queue_number, record_locator)
        response_data = self.__request_wrapper("queue place", request_data, self.endpoint)
        gds_response = SabreQueuePlaceExtractor(response_data).extract()
        return gds_response

    def ignore_transaction(self, token: str):
        """
        This function is for ignore transaction
        """
        request_data = self.xml_builder.ignore_transaction_rq(token)
        response_data = self.__request_wrapper("ignore transaction", request_data, self.endpoint)
        gds_response = SabreIgnoreTransactionExtractor(response_data).extract()
        return gds_response

    def is_ticket_exchangeable(self, token: str, ticket_number):
        """
        A method to check if the ticket number is exchangeable
        :param token: the security token
        :param ticket_number: the ticket number
        :return:
        """
        electronic_document_request = self.xml_builder.electronic_document_rq(token, ticket_number)
        electronic_document_response = self.__request_wrapper("is_ticket_exchangeable", electronic_document_request, self.endpoint)
        gds_response = IsTicketExchangeableExtractor(electronic_document_response).extract()
        return gds_response

    def exchange_shopping(self, token: str, pnr, passengers: list = [], origin_destination: list = []):
        """
        A method to search for applicable itinerary reissue options for an existing ticket
        :param token: the security token
        :param pnr: the Record locator
        :param passengers: passengers information
        :param origin_destination: itineraries information
        :return:
        """
        exchange_shopping_request = self.xml_builder.exchange_shopping_rq(token, pnr, passengers, origin_destination)
        exchange_shopping_response = self.__request_wrapper("exchange_shopping", exchange_shopping_request, self.endpoint)
        gds_response = ExchangeShoppingExtractor(exchange_shopping_response).extract()
        return gds_response

    def exchange_price(self, token: str, ticket_number, name_number, passenger_type):
        """
        A method to price an air ticket exchange
        :param token: the security token
        :param ticket_number: the ticket number
        :param name_number: the passenger name number
        :param passenger_type: the passenger type
        :return:
        """
        exchange_price_request = self.xml_builder.automated_exchanges_price_rq(token, ticket_number, name_number, passenger_type)
        exchange_price_response = self.__request_wrapper("exchange_price", exchange_price_request, self.endpoint)
        gds_response = ExchangePriceExtractor(exchange_price_response).extract()
        return gds_response

    def exchange_commit(self, token: str, price_quote, form_of_payment, fare_type, percent, amount):
        """
        A method to price an air ticket exchange
        :param token: the security token
        :param price_quote: the pq number
        :param form_of_payment: the type of payment
        :param fare_type: the fare type
        :param percent: the value of commission
        :param amount: the value of amount
        :return:
        """
        exchange_commit_request = self.xml_builder.automated_exchanges_commmit_rq(token, price_quote, form_of_payment, fare_type, percent, amount)
        exchange_commit_response = self.__request_wrapper("exchange_commit", exchange_commit_request, self.endpoint)
        gds_response = ExchangeCommitExtractor(exchange_commit_response).extract()
        return gds_response

    def create_pnr_rq(self, token: str, create_pnr_request):
        """
        the create pnr request builder
        Arguments:
            token : the security token
            create_pnr_request {[CreatPnrRequest]} -- [the pnr request]

        Returns:
            [GdsResponse] -- [create pnr response ]
        """

        request_data = self.json_builder.create_pnr_builder(create_pnr_request)
        response = self._rest_request_wrapper(request_data, "/v2.1.0/passenger/records?mode=create", token)
        gds_response = CreatePnrExtractor(response.content).extract()
        return gds_response

    def seat_map(self, token: str, flight_request: FlightSeatMap):
        """[This function will return the result for the seat map request]

        Arguments:
            token {[str]} -- [the security token]
            flight_request {[FlightSeatMap]} -- [this will handler the flight request]
        """
        seat_map_request = self.xml_builder.seap_map_rq(token, flight_request)
        seat_map_response = self.__request_wrapper("seat_map", seat_map_request, self.endpoint)
        gds_response = SeatMapResponseExtractor(seat_map_response).extract()
        return gds_response

    def update_passenger(self, token: str, pnr: str, passenger_update: PassengerUpdate):
        """
        Arguments:
            token {str} -- [ the security token]
            pnr {str} -- [ the pnr code ]
            passenger_update {[PassengerUpdate]} -- [the element to update]
        """
        update_passenger_request = self.xml_builder.update_passenger_rq(token, pnr, passenger_update)
        update_passenger_response = self._soap_request_wrapper(update_passenger_request)
        gds_response = UpdatePassengerExtractor(update_passenger_response.content).extract()
        return gds_response

    def revalidate_itinerary(self, token: str = None, itineraries: list = [], passengers: list = [], fare_type: str = None):
        """
        The Revalidate Itinerary (revalidate_itinerary) is used to recheck the availability and price of a
        specific itinerary option without booking the itinerary.
        The solution re-validates if the itinerary option is valid for purchase.
        Arguments:
            token{str} : the security token
            itineraries{list}: list itineraries
            passengers{list}: list passengers
            fare_type{str}: fare type(Net or Pub)

        Returns:
            [GdsResponse] -- [revalidate itinerary response]
        """
        revalidate_request = self.json_builder.revalidate_build(self.office_id, itineraries, passengers, fare_type)
        revalidate_response = self._rest_request_wrapper(revalidate_request, "/v4.3.0/shop/flights/revalidate", token)
        gds_response = RevalidateItineraryExtractor(revalidate_response.content).extract()
        return gds_response
