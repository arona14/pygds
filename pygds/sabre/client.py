import requests
import json
from pygds.core.client import BaseClient
from pygds.sabre.session import SabreSession
from pygds.sabre.xmlbuilders.builder import SabreXMLBuilder
from pygds.sabre.helpers import soap_service_to_json
from pygds.core.helpers import get_data_from_xml
from pygds.core.sessions import SessionInfo
from pygds.core.security_utils import generate_random_message_id
from pygds.sabre.jsonbuilders.builder import SabreJSONBuilder


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

    def open_session(self):
        """
        This will open a new session
        :return: a token session
        """
        open_session_xml = self.xml_builder.session_create_rq()
        response = self._soap_request_wrapper(open_session_xml)
        response = get_data_from_xml(response.content, "soap-env:Envelope", "soap-env:Header", "wsse:Security", "wsse:BinarySecurityToken")["#text"]
        return response

    def close_session(self):
        """
        A method to close a session
        :param pcc: The PCC
        :param conversation_id: the conversation id
        :param token_session: the token session
        :return: None
        """
        SabreSession().close()

    def get_reservation(self, pnr: str, pcc: str, conversation_id: str, need_close=True):
        """
        retrieve PNR
        :param pnr: the record locator
        :param pcc: the PCC
        :param conversation_id: The conversation id
        :param need_close: close or not the session
        :return: a Reservation object
        """
        try:
            token_session = self.open_session(pcc, conversation_id)

            get_reservation = SabreXMLBuilder().get_reservation_rq(pcc, conversation_id, token_session, pnr)
            response = requests.post(self.url, data=get_reservation, headers=self.headers)

            to_return = soap_service_to_json(response.content)
            to_return_dict = to_return

            if need_close:
                self.close_session(pcc, conversation_id, token_session)
        except:
            # TODO: Capture the real exception not the general one
            to_return_dict = None
        return to_return_dict

    def search_flightrq(self, message_id, request_search, available_flights_only, types):
        """
        This function is for searching flight
        :return : available flight for the specific request_search
        """

        request_data = self.json_builder.search_flight(request_search, available_flights_only, types)
        request_data = json.dumps(request_data, sort_keys=False, indent=4)
        _, _, token = self.get_or_create_session_details(message_id)
        if not token:
            self.log.info(f"Sorry but we didn't find a token with {message_id}. Creating a new one.")
            token = self.session_token()
            self.add_session(SessionInfo(token, None, None, message_id, False))
        else:
            if not message_id:
                message_id = generate_random_message_id()
            token = self.session_token()
            self.add_session(SessionInfo(token, None, None, message_id, False))
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
        return response
