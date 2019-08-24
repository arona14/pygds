# This file will be change for refactoring purpose.
# This file is for Sabre reservation classes and functions
# TODO: Use "import" statements for packages and modules only, not for individual classes or functions.
# Note that there is an explicit exemption for

import requests
import jxmlease
from pygds.core.client import BaseClient
from pygds.core.sessions import SessionInfo
from pygds.sabre.xmlbuilders.builder import SabreXMLBuilder
import json
from pygds.sabre.xml_parsers.response_extractor import PriceSearchExtractor
from pygds.core.security_utils import generate_random_message_id
from pygds.errors.gdserrors import NoSessionError

from pygds.sabre.formatters.reservation_formatter import SabreReservationFormatter
from pygds.sabre.formatters.reservation_formatter import BaseResponseExtractor
from pygds.sabre.jsonbuilders.builder import SabreBFMBuilder
from pygds.core.helpers import get_data_from_xml


class SabreClient(BaseClient):
    """
    A class to interact with Sabre GDS
    """

    def __init__(self, endpoint: str, rest_url, username: str, password: str, pcc: str, debug: bool = False):
        super().__init__(endpoint, username, password, pcc, debug)
        self.xml_builder = SabreXMLBuilder(endpoint, username, password, pcc)
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

        get_reservation = self.xml_builder.get_reservation_rq(token, pnr)
        response = requests.post(self.xml_builder.url, data=get_reservation, headers=self.header_template)
        to_return = SabreReservationFormatter(response.content)._extract()
        gds_response = BaseResponseExtractor(session_info, to_return, None)

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
        search_price_request = self.xml_builder.price_quote_rq(token_session, retain=str(retain).lower(), fare_type=fare_type, segment_select=segment_select, passenger_type=passenger_type, baggage=baggage, region_name=region_name)
        search_price_response = self.__request_wrapper("search_price_quote", search_price_request, self.xml_builder.url)
        print("search_price_response")
        print(search_price_response)
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
        store_price_request = self.xml_builder.price_quote_rq(token_session, retain=str(retain).lower(), fare_type=fare_type, segment_select=segment_select, passenger_type=passenger_type, baggage=baggage, region_name=region_name, brand_id=brand_id)
        search_price_response = self.__request_wrapper("store_price_quote", store_price_request, self.xml_builder.url)
        session_info = SessionInfo(token_session, sequence + 1, token_session, message_id, False)
        self.add_session(session_info)
        response = PriceSearchExtractor(search_price_response).extract()
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

    def search_flightrq(self, message_id, request_searh, types):
        """
        This function is for searching flight
        :return : available flight for the specific request_search
        """

        request_data = SabreBFMBuilder(request_searh).search_flight(types)
        request_data = json.dumps(request_data, sort_keys=False, indent=4)
        print(request_data)
        _, _, token = self.get_or_create_session_details(message_id)
        if not token:
            self.log.info(f"Sorry but we didn't find a token with {message_id}. Creating a new one.")
            token = self.session_token()
            print(token)
            self.add_session(SessionInfo(token, None, None, message_id, False))
        else:
            if not message_id:
                message_id = generate_random_message_id()
                print(message_id)
            token = self.session_token()
            self.add_session(SessionInfo(token, None, None, message_id, False))
            print(token)
            self.log.info("Waao you already have a token!")
        return self._rest_request_wrapper(request_data, "/v4.1.0/shop/flights?mode=live", token)

    def session_token(self):
        """
        This will open a new session
        :return: a Session token
        """
        open_session_xml = self.xml_builder.session_token_rq()
        response = self._request_wrapper(open_session_xml, None)
        response = get_data_from_xml(response.content, "soap-env:Envelope", "soap-env:Header", "wsse:Security", "wsse:BinarySecurityToken")["#text"]
        # print(response)
        return response


# if __name__ == "__main__":
# print(SabreClient().session_token())
