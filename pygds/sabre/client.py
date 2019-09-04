# This file will be change for refactoring purpose.
# This file is for Sabre reservation classes and functions
# TODO: Use "import" statements for packages and modules only, not for individual classes or functions.
# Note that there is an explicit exemption for
from pygds.sabre.json_parsers.response_extractor import CreatePnrExtractor
from pygds.sabre.jsonbuilders.builder import SabreJSONBuilder
from pygds.core.request import LowFareSearchRequest
from pygds.core.security_utils import generate_random_message_id
from pygds.core.helpers import get_data_from_xml
import json
from pygds.sabre.xml_parsers.response_extractor import PriceSearchExtractor, DisplayPnrExtractor, SendCommandExtractor, IssueTicketExtractor, EndTransactionExtractor, \
    SendRemarkExtractor, SabreQueuePlaceExtractor, SabreIgnoreTransactionExtractor, SeatMapResponseExtractor, IsTicketExchangeableExtractor, ExchangeShoppingExtractor, \
    ExchangePriceExtractor, ExchangeCommitExtractor, UpdatePassengerExtractor, RebookExtractor
from pygds.errors.gdserrors import NoSessionError
import jxmlease
import requests
from pygds.core.client import BaseClient
from pygds.core.sessions import SessionInfo
from pygds.sabre.xmlbuilders.builder import SabreXMLBuilder
from pygds.core.types import PassengerUpdate


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
        # if status == 500:
        #     error = ErrorExtractor(response.content).extract()
        #     sess, (faultcode, faultstring) = error.session_info, error.payload
        #     self.log.error(f"faultcode: {faultcode}, faultstring: {faultstring}")
        #     raise ServerError(sess, status, faultcode, faultstring)
        # elif status == 400:
        #     sess = SessionExtractor(response.content).extract()
        #     raise ClientError(sess, status, "Client Error")
        return response.content

    def open_session(self):
        """
        This will open a new session
        :return: a token session
        """
        message_id = generate_random_message_id()
        open_session_xml = self.xml_builder.session_create_rq()
        response = self._request_wrapper(open_session_xml, None)
        r = jxmlease.parse(response.content)
        print(r)
        token = r[u'soap-env:Envelope'][u'soap-env:Header'][u'wsse:Security'][u'wsse:BinarySecurityToken']
        session_info = SessionInfo(token, 1, token, message_id, False)
        self.add_session(session_info)
        return session_info

    def close_session(self, message_id):
        """
        A method to close a session
        :param token_session: the token session
        :return: None
        """
        # SabreSession().close()
        pass

    def get_reservation(self, pnr: str, message_id: str, need_close=True):
        """retrieve PNR
        :param pnr: the record locator
        :param message_id: the message identifier
        :param need_close: close or not the session
        :return: a Reservation object
        """
        _, _, token = self.get_or_create_session_details(message_id)
        session_info = None
        if not token:
            session_info = self.open_session()
            token = session_info.security_token

        display_pnr_request = self.xml_builder.get_reservation_rq(token, pnr)
        display_pnr_response = self.__request_wrapper("get_reservation", display_pnr_request, self.xml_builder.url)
        gds_response = DisplayPnrExtractor(display_pnr_response).extract()
        gds_response.session_info = session_info

        if need_close:
            self.close_session(message_id)

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
        :param  pcc : the pcc
        :param region_name: the region name
        :return:
        """
        _, sequence, token_session = self.get_or_create_session_details(message_id)
        if token_session is None:
            raise NoSessionError(message_id)
        search_price_request = self.xml_builder.price_quote_rq(token_session, retain=retain, fare_type=fare_type, segment_select=segment_select, passenger_type=passenger_type, baggage=baggage, region_name=region_name)
        search_price_response = self.__request_wrapper("search_price_quote", search_price_request, self.endpoint)
        session_info = SessionInfo(token_session, sequence + 1, token_session, message_id, False)
        self.add_session(session_info)
        response = PriceSearchExtractor(search_price_response).extract()
        response.session_info = session_info
        return response

    def store_price_quote(self, message_id, retain: bool = True, fare_type: str = '', segment_select: list = [], passenger_type: list = [], baggage: int = 0, region_name: str = "", brand_id: str = None):
        """
        A method to store price
        :param message_id: the message id
        :param retain: the retain value
        :param fare_type: the fare type value value
        :param segment_select: the list of segment selected
        :param  passenger_type: the list of passenger type selected
        :param baggage: number of baggage
        :param  pcc : the pcc
        :param region_name: the region name
        :param brand_id
        :return:
        """
        _, sequence, token_session = self.get_or_create_session_details(message_id)
        if token_session is None:
            raise NoSessionError(message_id)
        store_price_request = self.xml_builder.price_quote_rq(token_session, retain=retain, fare_type=fare_type, segment_select=segment_select, passenger_type=passenger_type, baggage=baggage, region_name=region_name, brand_id=brand_id)
        store_price_response = self.__request_wrapper("store_price_quote", store_price_request, self.endpoint)
        session_info = SessionInfo(token_session, sequence + 1, token_session, message_id, False)
        self.add_session(session_info)
        response = PriceSearchExtractor(store_price_response).extract()
        response.session_info = session_info
        return response

    def cancel_list_segment(self, token_session, list_segment):
        """
        A method to cancel segment
        :param token_session: the token session
        :param retain: the token session
        :param commission: the commission is used to specify the numeric amount or  the precentage of commission being claimed if applicable
        :param tour_code: the token session
        :param fare_type: the token session
        :param ticket_designator: the token session
        :param segment_number: the segment number is used to instruct the system to price specified itinerary segments
        :param name_select: the name select is used to instruct the system to price theitinerary based upon a particular name field
        :param passenger_type: the passenger type is used to specify a passenger type code.
        :param plus_up: the plus up is used to specify an amount to add on top of the fare
        """
        return self.xml_builder.cancel_segment_rq(token_session, list_segment)

    def search_flight(self, message_id, search_request: LowFareSearchRequest, available_only: bool, types: str):
        """
        This function is for searching flight
        :return : available flight for the specific request_search
        """
        _, _, session_info = self.get_or_create_session_details(message_id)
        search_flight_request = self.json_builder.search_flight_builder(search_request, available_only, types)
        if not session_info:
            self.log.info(f"Sorry but we didn't find a token with {message_id}. Creating a new one.")
            session_info = self.new_rest_token()
        else:
            session_info = self.new_rest_token()
            self.log.info("Waao you already have a token!")
        search_response = self._rest_request_wrapper(json.dumps(search_flight_request), "/v4.1.0/shop/flights?mode=live", session_info.security_token)
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
        session_info = SessionInfo(token, 1, message_id, token, False)
        return session_info

    def issue_ticket(self, message_id, price_quote, code_cc=None, expire_date=None, cc_number=None, approval_code=None, payment_type=None, commission_value=None):
        """
        This function is make for the ticket process.
        she does not want to make the end transaction at the end to commit the change
        :return
        """
        _, sequence, token_session = self.get_or_create_session_details(message_id)
        if token_session is None:
            raise NoSessionError(message_id)
        # self.send_command_befor_issue_ticket(message_id)
        request_data = self.xml_builder.air_ticket_rq(token_session, price_quote, code_cc, expire_date, cc_number, approval_code, payment_type, commission_value)
        response_data = self.__request_wrapper("air_ticket_rq", request_data, self.endpoint)
        return IssueTicketExtractor(response_data).extract()

    def end_transaction(self, message_id):
        """
        This function is for end transaction
        """
        _, sequence, token_session = self.get_or_create_session_details(message_id)
        if token_session is None:
            raise NoSessionError(message_id)
        request_data = self.xml_builder.end_transaction_rq(token_session)
        response_data = self.__request_wrapper("end_transaction", request_data, self.endpoint)
        session_info = SessionInfo(token_session, sequence + 1, token_session, message_id, False)
        self.add_session(session_info)
        gds_response = EndTransactionExtractor(response_data).extract()
        gds_response.session_info = session_info
        return gds_response

    def send_remark(self, message_id, text):
        """this will send a remark for a pnr
        :param message_id: the messgae id
        :param text: the remark text
        :return:
        """
        _, sequence, token_session = self.get_or_create_session_details(message_id)
        if token_session is None:
            raise NoSessionError(message_id)
        send_remark_request = self.xml_builder.send_remark_rq(token_session, text)
        send_remark_response = self.__request_wrapper("send_remark", send_remark_request, self.endpoint)
        session_info = SessionInfo(token_session, sequence + 1, token_session, message_id, False)
        self.add_session(session_info)
        response = SendRemarkExtractor(send_remark_response).extract()
        response.session_info = session_info
        return response

    def re_book_air_segment(self, message_id, flight_segment, pnr):
        """
        A method to rebook air segment
        :param message_id: the message id
        :param flight_segment: list of flight segment
        :param pnr: the pnr
        :param number_in_party: the number of passenger
        :return:
        """
        _, sequence, token_session = self.get_or_create_session_details(message_id)
        if token_session is None:
            raise NoSessionError(message_id)
        re_book_air_segment_request = self.xml_builder.re_book_air_segment_rq(token_session, flight_segment, pnr)
        re_book_air_segment_response = self.__request_wrapper("re_book_air_segment", re_book_air_segment_request, self.endpoint)
        session_info = SessionInfo(token_session, sequence + 1, token_session, message_id, False)
        self.add_session(session_info)
        response = RebookExtractor(re_book_air_segment_response).extract()
        response.session_info = session_info
        return response

    def send_command(self, message_id: str, command: str):
        """send command
        :param message_id: the message identifier
        :param command: the value of the command
        """
        _, sequence, token_session = self.get_or_create_session_details(message_id)
        if token_session is None:
            raise NoSessionError(message_id)
        command_request = self.xml_builder.sabre_command_lls_rq(token_session, command)
        command_response = self.__request_wrapper("send_command", command_request, self.endpoint)
        session_info = SessionInfo(token_session, sequence + 1, token_session, message_id, False)
        self.add_session(session_info)
        gds_response = SendCommandExtractor(command_response).extract()
        gds_response.session_info = session_info
        return gds_response

    def queue_place(self, message_id: str, queue_number: str, record_locator: str):
        """This function is for queue place
        """
        _, sequence, token_session = self.get_or_create_session_details(message_id)
        if token_session is None:
            raise NoSessionError(message_id)
        request_data = self.xml_builder.queue_place_rq(token_session, queue_number, record_locator)
        response_data = self.__request_wrapper("queue place", request_data, self.endpoint)
        session_info = SessionInfo(token_session, sequence + 1, token_session, message_id, False)
        self.add_session(session_info)
        gds_response = SabreQueuePlaceExtractor(response_data).extract()
        gds_response.session_info = session_info
        return gds_response

    def ignore_transaction(self, message_id: str):
        """
        This function is for ignore transaction
        """
        _, sequence, token_session = self.get_or_create_session_details(message_id)
        if token_session is None:
            raise NoSessionError(message_id)
        request_data = self.xml_builder.ignore_transaction_rq(token_session)
        response_data = self.__request_wrapper("ignore transaction", request_data, self.endpoint)
        session_info = SessionInfo(token_session, sequence + 1, token_session, message_id, False)
        self.add_session(session_info)
        gds_response = SabreIgnoreTransactionExtractor(response_data).extract()
        gds_response.session_info = session_info
        return gds_response

    def is_ticket_exchangeable(self, message_id, ticket_number):
        """
        A method to check if the ticket number is exchangeable
        :param message_id: the message id
        :param ticket_number: the ticket number
        :return:
        """
        _, sequence, token_session = self.get_or_create_session_details(message_id)
        if token_session is None:
            raise NoSessionError(message_id)
        electronic_document_request = self.xml_builder.electronic_document_rq(token_session, ticket_number)
        electronic_document_response = self.__request_wrapper("is_ticket_exchangeable", electronic_document_request, self.endpoint)
        session_info = SessionInfo(token_session, sequence + 1, token_session, message_id, False)
        self.add_session(session_info)
        gds_response = IsTicketExchangeableExtractor(electronic_document_response).extract()
        gds_response.session_info = session_info
        return gds_response

    def exchange_shopping(self, message_id, pnr, passengers: list = [], origin_destination: list = []):
        """
        A method to search for applicable itinerary reissue options for an existing ticket
        :param message_id: the message id
        :param passengers: passengers informations
        :param origin_destination: itineraries informations
        :return:
        """
        _, sequence, token_session = self.get_or_create_session_details(message_id)
        if token_session is None:
            raise NoSessionError(message_id)
        exchange_shopping_request = self.xml_builder.exchange_shopping_rq(token_session, pnr, passengers, origin_destination)
        exchange_shopping_response = self.__request_wrapper("exchange_shopping", exchange_shopping_request, self.endpoint)
        session_info = SessionInfo(token_session, sequence + 1, token_session, message_id, False)
        self.add_session(session_info)
        gds_response = ExchangeShoppingExtractor(exchange_shopping_response).extract()
        gds_response.session_info = session_info
        return gds_response

    def exchange_price(self, message_id, ticket_number, name_number, passenger_type):
        """
        A method to price an air ticket exchange
        :param message_id: the message id
        :param ticket_number: the ticket number
        :param name_number: the passenger name number
        :param passenger_type: the passenger type
        :return:
        """
        _, sequence, token_session = self.get_or_create_session_details(message_id)
        if token_session is None:
            raise NoSessionError(message_id)
        exchange_price_request = self.xml_builder.automated_exchanges_price_rq(token_session, ticket_number, name_number, passenger_type)
        exchange_price_response = self.__request_wrapper("exchange_price", exchange_price_request, self.endpoint)
        session_info = SessionInfo(token_session, sequence + 1, token_session, message_id, False)
        self.add_session(session_info)
        gds_response = ExchangePriceExtractor(exchange_price_response).extract()
        gds_response.session_info = session_info
        return gds_response

    def exchange_commit(self, message_id, price_quote, form_of_payment, fare_type, percent, amount):
        """
        A method to price an air ticket exchange
        :param message_id: the message id
        :param price_quote: the pq number
        :param form_of_payment: the type of payment
        :param fare_type: the fare type
        :param percent: the value of commission
        :param amount: the value of amount
        :return:
        """
        _, sequence, token_session = self.get_or_create_session_details(message_id)
        if token_session is None:
            raise NoSessionError(message_id)
        exchange_commit_request = self.xml_builder.automated_exchanges_commmit_rq(token_session, price_quote, form_of_payment, fare_type, percent, amount)
        exchange_commit_response = self.__request_wrapper("exchange_commit", exchange_commit_request, self.endpoint)
        session_info = SessionInfo(token_session, sequence + 1, token_session, message_id, False)
        self.add_session(session_info)
        gds_response = ExchangeCommitExtractor(exchange_commit_response).extract()
        return gds_response

    def create_pnr_rq(self, message_id, create_pnr_request):
        """
        the create pnr request builder
        Arguments:
            message_id : the messgae id
            create_pnr_request {[CreatPnrRequest]} -- [the pnr request]

        Returns:
            [GdsResponse] -- [create pnr response ]
        """
        request_data = self.json_builder.create_pnr_builder(create_pnr_request)
        _, _, token = self.get_or_create_session_details(message_id)
        if not token:
            self.log.info(f"Sorry but we didn't find a token with {message_id}. Creating a new one.")
            token = self.new_rest_token()
            session_info = SessionInfo(token, None, None, message_id, False)
            self.add_session(session_info)

        response = self._rest_request_wrapper(request_data, "/v2.1.0/passenger/records?mode=create", token.security_token)
        gds_response = CreatePnrExtractor(response.content).extract()
        gds_response.session_info = session_info
        return gds_response

    def seat_map(self, message_id, flight_request):
        """[This function will return the result for the seat map request]

        Arguments:
            message_id {[str]} -- [the message id for the communication]
            flight_request {[object]} -- [this will handler the flight request]
        """
        _, sequence, token_session = self.get_or_create_session_details(message_id)
        print(token_session)
        if token_session is None:
            raise NoSessionError(message_id)
        seat_map_request = self.xml_builder.seap_map_rq(token_session, flight_request)
        search_price_response = self._soap_request_wrapper(seat_map_request)
        session_info = SessionInfo(token_session, sequence + 1, token_session, message_id, False)
        self.add_session(session_info)
        gds_response = SeatMapResponseExtractor(search_price_response.content).extract()
        gds_response.session_info = session_info
        return gds_response

    def update_passenger(self, message_id: str, pnr: str, passenger_updt: PassengerUpdate):
        """
        Arguments:
            message_id {str} -- [ the message id ]
            pnr {str} -- [ the pnr code ]
            passenger_updt {[PassengerUpdate]} -- [the element to update]
        """
        _, sequence, token_session = self.get_or_create_session_details(message_id)
        print(token_session)
        if token_session is None:
            raise NoSessionError(message_id)
        update_passenger_request = self.xml_builder.update_passenger_rq(token_session, pnr, passenger_updt)
        update_passenhger_response = self._soap_request_wrapper(update_passenger_request)
        session_info = SessionInfo(token_session, sequence + 1, token_session, message_id, False)
        self.add_session(session_info)
        gds_response = UpdatePassengerExtractor(update_passenhger_response.content).extract()
        gds_response.session_info = session_info
        return gds_response
