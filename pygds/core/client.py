import logging
from datetime import datetime

import requests
from requests import Response

from pygds.core.price import PriceRequest
from pygds.core.sessions import MemorySessionHolder, SessionInfo, TokenType


class BaseClient:
    """
        This is the main class to make calls to API of GDS
    """
    def __init__(self, endpoint: str, username: str, password: str, office_id: str, debug: bool = False):
        """
        Init the GDS
        :param endpoint: The url of the endpoint. It can be on test, or production
        :param username: The username to authenticate to the Amadeus Server
        :param password: The password to authenticate to the Amadeus Server
        :param office_id: The office_id (or PCC)
        :param debug: Telling if the client is debugging requests and responses.
    """
        self.endpoint = endpoint
        self.username = username
        self.password = password
        self.office_id = office_id
        self.session_holder = MemorySessionHolder()
        self.header_template = {'Content-Type': 'text/xml;charset=UTF-8', 'Accept-Encoding': 'gzip,deflate'}
        self.is_debugging = debug
        self.log = logging.getLogger(str(self.__class__))

    def get_session_info(self, message_id) -> SessionInfo:
        """
        get the session info associated to the message id
        :param message_id: The message id
        :return: SessionInfo
        """
        return self.session_holder.get_session_info(message_id)

    def get_or_create_session_details(self, message_id) -> tuple:
        """
        get session details as tuple if exists, otherwise return empty ones.
        :param message_id: The message id associated to the supposed session
        :return: tuple(session_id, sequence_number, security_token) or (None, None, None)
        """
        session = self.get_session_info(message_id)
        if session is None:
            return None, None, None
        else:
            seq = session.sequence_number if session.sequence_number else 0
            return session.session_id, seq + 1, session.security_token

    def add_session(self, session_info: SessionInfo) -> bool:
        """
        Add a session info to the holder
        :param session_info: SessionInfo info object
        :return: bool (telling whether or not this is added)
        """
        if session_info is None or session_info.session_ended is True:
            return False
        else:
            session_info.last_access = datetime.now()
            self.session_holder.add_session(session_info)
            return True

    def _request_wrapper(self, request_data, soap_action) -> Response:
        """
            This wrapper method helps wrap request with
        """
        headers = self.header_template
        headers["SOAPAction"] = soap_action
        return requests.post(self.endpoint, data=request_data, headers=headers)

    def start_new_session(self):
        pass

    def close_session(self, message_id, remove_session: bool = False):
        """
        Will close an session corresponding to the given message id
        :param message_id: str -> The message id
        :param remove_session: bool -> tell if we need to remove it from holder
        :return:
        """
        pass

    def end_transaction(self, message_id):
        """
        Commit actions done in the current transaction of the token
        :param message_id: The message id associated to the token
        :return:
        """
        pass

    def fare_master_pricer_travel_board_search(self, origin, destination, departure_date, arrival_date):
        pass

    def fare_price_pnr_with_booking_class(self, message_id, price_request: PriceRequest):
        pass

    def send_command(self, command: str, message_id: str = None, close_trx: bool = False):
        pass

    def new_rest_token(self):
        pass

    def close_rest_token(self, message_id):
        pass

    def close_expired_sessions(self, leeway: datetime):
        """
        This method will close all sessions not used since leeway
        :param leeway: The date from which see not used tokens
        :return:
        """
        for session in self.session_holder.get_expired_sessions(leeway):
            message_id = session.message_id
            if session.token_type == TokenType.SESSION_TOKEN:
                self.close_session(message_id)
            elif session.token_type == TokenType.REST_TOKEN:
                self.close_rest_token(message_id)
            else:
                self.log.warning(f"Unknown token type with message id {message_id}. Will continue to hold "
                                 f"this session.")
                continue
            self.session_holder.remove_session(message_id)
            self.log.info(f"Token associated to message id {message_id} is closed")


class ClientPool:
    """
        This class is for handling a pool of client
    """
    def __init__(self):
        self.clients = {}

    def add_client(self, client: BaseClient):
        """ Add a client to the pool """
        if client is None:
            raise ValueError("The client object cannot be null")
        self.clients[client.office_id] = client

    def get_client(self, office_id: str) -> BaseClient:
        """ Get the client form the pool by giving the :office_id:. Will return None if not found."""
        try:
            return self.clients[office_id]
        except KeyError:
            return None
