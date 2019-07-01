from .xmlbuilders.builder import AmadeusXMLBuilder
import requests
import jxmlease


class AmadeusClient():
    """
        This is the main class to make calls to Amadeus API
    """
    def __init__(self, endpoint: str, username: str, password: str, office_id: str, wsap: str):
        self.endpoint = endpoint
        self.username = username
        self.password = password
        self.office_id = office_id
        self.xmlbuilder: AmadeusXMLBuilder = AmadeusXMLBuilder(endpoint, username, password, office_id, wsap)
        self.header_template = {'Content-Type': 'text/xml;charset=UTF-8', 'Accept-Encoding': 'gzip,deflate'}

    def __request_wrapper(self, method_name, request_data, soap_action):
        headers = self.header_template
        headers["SOAPAction"] = soap_action
        response = requests.post(self.endpoint, data=request_data, headers=headers)
        status = response.status_code
        print(f"{method_name} status: {status}")
        response_data = jxmlease.parse(response.content)
#        if status == 500:
#            # handle errors by building the correspondig Exception object
#            raise ValueError(f'Error with status {status}')
        return response_data

    def start_new_session(self):
        request_data = self.xmlbuilder.start_transaction(None, self.office_id, self.username, self.password, None, None)
        response_data = self.__request_wrapper("start_new_session", request_data, 'http://webservices.amadeus.com/VLSSOQ_04_1_1A')
        return response_data

    def fare_master_pricer_travel_board_search(self, origin, destination, departure_date, arrival_date):
        request_data = self.xmlbuilder.fare_master_pricer_travel_board_search(self.office_id, origin, destination, departure_date, arrival_date)
        response_data = self.__request_wrapper("fare_master_pricer_travel_board_search", request_data, 'http://webservices.amadeus.com/FMPTBQ_18_1_1A')
        return response_data

    def fare_price_pnr_with_booking_class(self, message_id, session_id, sequence_number, security_token):
        request_data = self.xmlbuilder.fare_price_pnr_with_booking_class(message_id, session_id, sequence_number, security_token)
        response_data = self.__request_wrapper("fare_price_pnr_with_booking_class", request_data, 'http://webservices.amadeus.com/TPCBRQ_18_1_1A')
        return response_data
