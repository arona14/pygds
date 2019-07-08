# coding: utf-8
import requests
from ..core import xmlparser

from .errors import ClientError, ServerError
from .xmlbuilders.builder import AmadeusXMLBuilder
from .amadeus_types import AmadeusSessionInfo


class AmadeusClient:
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
        """
            This wrapper method helps wrap request with:
            1- creating request and calling it
            2- read status code
            3- look status code and handle exceptions
            4- parse response and return it
        """
        headers = self.header_template
        headers["SOAPAction"] = soap_action
        response = requests.post(self.endpoint, data=request_data, headers=headers)
        status = response.status_code
        print(f"{method_name} status: {status}")
        response_data = xmlparser.parse_xml(response.content)
        if status == 500:
            faultcode, faultstring = xmlparser.extract_single_elements(response_data, "//faultcode/text()", "//faultstring/text()")
            print(f"faultcode: {faultcode}, faultstring: {faultstring}")
            raise ServerError(status, faultcode, faultstring)
        elif status == 400:
            raise ClientError(status, "Client Error")
        return response_data

    def start_new_session(self):
        """
            This method starts a new session to Amadeus
        """
        request_data = self.xmlbuilder.start_transaction(None, self.office_id, self.username, self.password, None, None)
        response_data = self.__request_wrapper("start_new_session", request_data, 'http://webservices.amadeus.com/VLSSOQ_04_1_1A')
        seq, tok, ses = xmlparser.extract_single_elements(response_data, "//*[local-name()='SequenceNumber']/text()", "//*[local-name()='SecurityToken']/text()", "//*[local-name()='SessionId']/text()")
        return AmadeusSessionInfo(tok, seq, ses)

    def get_reservation(self, pcc, conversation_id, token_session, record_locator, end_session=True):
        """
            Return the reservation data from PNR.
        """
        request_data = self.xmlbuilder.get_reservation_builder(pcc, conversation_id, token_session, record_locator, end_session)
        response_data = self.__request_wrapper("get_reservation", request_data, 'http://webservices.amadeus.com/PNRRET_17_1_1A')
        return response_data
    
    def add_form_of_payment(self, message_id, session_id, sequence_number, security_token, form_of_payment, passenger_reference_type, passenger_reference_value, form_of_payment_sequence_number, form_of_payment_code, group_usage_attribute_type, company_code, form_of_payment_type, vendor_code, carte_number, security_id, expiry_date):
        """
            add the payment form to the PNR.
        """
        request_data = self.xmlbuilder.add_form_of_payment_builder( message_id, session_id, sequence_number, security_token, form_of_payment, passenger_reference_type, passenger_reference_value, form_of_payment_sequence_number, form_of_payment_code, group_usage_attribute_type, company_code, form_of_payment_type, vendor_code, carte_number, security_id, expiry_date)
        response_data = self.__request_wrapper("add_form_of_payment", request_data, 'http://webservices.amadeus.com/TFOPCQ_15_4_1A')
        return response_data 

    def pnr_add_multi_element(self, session_id, sequence_number, security_token, message_id, option_code, segment_name, identification, credit_card_code, account_number, expiry_date, currency_code):
        """
            add multi elements to the PNR. 
        """
        request_data = self.xmlbuilder.pnr_add_multi_element_builder(session_id, sequence_number, security_token, message_id, option_code, segment_name, identification, credit_card_code, account_number, expiry_date, currency_code)
        response_data = self.__request_wrapper("pnr_add_multi_element", request_data, 'http://webservices.amadeus.com/PNRADD_17_1_1A')
        return response_data

    def ticketing_pnr(self, message_id, session_id, sequence_number, security_token, passenger_reference_type, passenger_reference_value):
        """
            PNR ticketing process. 
        """ 
        request_data = self.xmlbuilder.ticket_pnr_builder(message_id, session_id, sequence_number, security_token, passenger_reference_type, passenger_reference_value)
        response_data = self.__request_wrapper("ticketing_pnr", request_data, 'http://webservices.amadeus.com/TTKTIQ_15_1_1A')
        return response_data

    def fare_master_pricer_travel_board_search(self, origin, destination, departure_date, arrival_date):
        """
            A method for searching prices of an itinerary
        """
        request_data = self.xmlbuilder.fare_master_pricer_travel_board_search(self.office_id, origin, destination, departure_date, arrival_date)
        response_data = self.__request_wrapper("fare_master_pricer_travel_board_search", request_data, 'http://webservices.amadeus.com/FMPTBQ_18_1_1A')
        return response_data

    def fare_price_pnr_with_booking_class(self, message_id, session_id, sequence_number, security_token):
        """
            Price a PNR with a booking class.
            The PNR is supposed to be supplied in the session on a previous call
        """
        request_data = self.xmlbuilder.fare_price_pnr_with_booking_class(message_id, session_id, sequence_number, security_token)
        response_data = self.__request_wrapper("fare_price_pnr_with_booking_class", request_data, 'http://webservices.amadeus.com/TPCBRQ_18_1_1A')
        return response_data
