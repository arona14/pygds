import logging

import requests

from pygds.core.sessions import SessionHolder


class BaseClient:
    """
        This is the main class to make calls to API of GDS
        :param endpoint: The url of the endpoint. It can be on test, or production
        :param username: The username to authenticate to the Amadeus Server
        :param password: The password to authenticate to the Amadeus Server
        :param office_id: The office_id (or PCC)
        :param debug: Telling if the client is debugging requests and responses.
    """
    def __init__(self, endpoint: str, username: str, password: str, office_id: str, debug: bool = False):
        self.endpoint = endpoint
        self.username = username
        self.password = password
        self.office_id = office_id
        self.session_holder = SessionHolder()
        self.header_template = {'Content-Type': 'text/xml;charset=UTF-8', 'Accept-Encoding': 'gzip,deflate'}
        self.is_debugging = debug
        self.log = logging.getLogger(str(self.__class__))

    def get_session_info(self, message_id):
        return self.session_holder.get_session_info(message_id)

    def get_or_create_session_info(self, message_id):
        session = self.get_session_info(message_id)
        if session is None:
            return None, None, None
        else:
            return session.session_id, session.sequence_number + 1, session.security_token

    def _request_wrapper(self, request_data, soap_action):
        """
            This wrapper method helps wrap request with
        """
        headers = self.header_template
        headers["SOAPAction"] = soap_action
        return requests.post(self.endpoint, data=request_data, headers=headers)

    def start_new_session(self):
        pass

    def end_session(self, session_id):
        pass

    def fare_master_pricer_travel_board_search(self, origin, destination, departure_date, arrival_date):
        pass

    def fare_price_pnr_with_booking_class(self, message_id):
        pass

    def send_command(self, command: str, message_id: str = None, close_trx: bool = False):
        pass


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

    def get_client(self, office_id: str):
        """ Get the client form the pool by giving the :office_id:. Will return None if not found."""
        try:
            return self.clients[office_id]
        except KeyError:
            return None
