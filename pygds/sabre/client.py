# This file will be change for refactoring purpose.
# This file is for Sabre reservation classes and functions
# TODO: Use "import" statements for packages and modules only, not for individual classes or functions.
# Note that there is an explicit exemption for

import requests,jxmlease
from pygds.core.client import BaseClient
from pygds.core.request import  LowFareSearchRequest
from pygds.core.sessions import SessionInfo
from pygds.sabre.xmlbuilders.builder import SabreXMLBuilder
from pygds.sabre.helpers import get_data_from_json as from_json
from pygds.sabre.jsonbuilders.builder import  SabreBFMBuilder
from pygds.core.app_error import ApplicationError

from pygds.sabre.xml_parsers.response_extractor import PriceSearchExtractor, IssueTicketExtractor


class SabreClient(BaseClient):
    """
    A class to interact with Sabre GDS
    """
    def __init__(self, url: str, username: str, password: str, pcc: str, debug: bool = False):
        super().__init__(url, username, password, pcc, debug)
        self.xml_builder = SabreXMLBuilder(url, username, password, pcc)
        self.header_template = {'content-type': 'text/xml; charset=utf-8'}


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
        # print(response.content)
        # status = response.status_code
        # if self.is_debugging:
        #     self.log.debug(request_data)
        #     self.log.debug(response.content)
        #     self.log.debug(f"{method_name} status: {status}")
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
        message_id = "Virginie"
        open_session_xml = self.xml_builder.session_create_rq()
        response = self._request_wrapper(open_session_xml, None)
        r = jxmlease.parse(response.content)
        token = r[u'soap-env:Envelope'][u'soap-env:Header'][u'wsse:Security'][u'wsse:BinarySecurityToken']
        session_info = SessionInfo(token, 1, token, message_id, False)
        self.add_session(session_info)
        return session_info

    def close_session(self,token_session):
        """
        A method to close a session
        :param token_session: the token session
        :return: None
        """
        return self.xml_builder.session_close_rq(token_session)

    def get_reservation(self,pnr:str, message_id:str ,need_close = True):
        """
        retrieve PNR
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

        to_return = from_json(response.content,"stl18:GetReservationRS")
  
        if need_close:
            self.close_session(token)

        return to_return
        
    def search_price_quote(self, message_id, retain:bool=False, fare_type:str='', segment_select:list=[], passenger_type:list=[],baggage:int=0, pcc:str="", region_name:str=""):
        """
        A method to cancel segment
        :param message_id: the message id 
        :return: None
        """
        print('search_price_quote')
        _, _, token_session = self.get_or_create_session_details(message_id)
        session_info = None
        if not token_session:
            session_info = self.open_session()
            token_session = session_info.security_token

        segment_number = self._get_segment_number(segment_select)
        fare_type_value = self._get_fare_type(fare_type) if self._get_fare_type(fare_type) else ""
        passenger_type, name_select = self._get_passenger_type(passenger_type, fare_type) 
        commission = self._get_commision(baggage, pcc, region_name)
        
        token_session="Shared/IDL:IceSess\\/SessMgr:1\\.0.IDL/Common/!ICESMS\\/RESC!ICESMSLB\\/RES.LB!-2983069682133371008!1701442!0"
        search_price_request = self.xml_builder.price_quote_rq(token_session,retain=str(retain).lower(), commission=commission, fare_type=fare_type_value, segment_select=segment_number, name_select=name_select, passenger_type=passenger_type)
        
        
        search_price_response = self.__request_wrapper("search_price_quote", search_price_request,
                                               self.xml_builder.url)
        #response =  requests.post(self.xml_builder.url, data=search_price, headers=self.header_template)
        return PriceSearchExtractor(search_price_response).extract()
 

    def _get_segment_number(self, segment_select):
        if segment_select != []:
            segment_number = "<ItineraryOptions>"
            for k in segment_select:
                segment_number = segment_number+"<SegmentSelect Number='"+str(k)+"'/>" 
            segment_number = segment_number+"</ItineraryOptions>"
            return segment_number
        return None


    def _get_fare_type(self, fare_type):
        if fare_type == "Pub":
            fare_type_value = "<Account>"
            fare_type_value = fare_type_value+"<Code>COM</Code>" 
            fare_type_value = fare_type_value+"</Account>"
            return fare_type_value
        return None


    def _get_passenger_type(self, passenger_type, fare_type):

        child_list = ["CNN","JNN","J12","J11","J10","J09","J08","J07","J06","J05","J04","J03","J02","C12","C11","C10","C09","C08","C07","C06","C05","C04","C03","C02"]
        for pax in passenger_type:
            if fare_type == "Pub":
                if pax['code'] in ["ADT","JCB"]:
                    pax_type = f"""<PassengerType Code="ADT" Quantity="{pax["quantity"]}"/>"""
                
                elif pax_type['code'] in child_list:
                    code = "C"+str(pax['code'][-2:])
                    pax_type = "<PassengerType Code='"+code+ "' Quantity='" +pax['quantity'] + "'/>" 
                
                elif pax['code'] in ["INF","JNF"]:
                    pax_type = f"""<PassengerType Code="INF" Quantity="{pax["quantity"]}"/>"""

            elif fare_type == "Net":
                if pax['code'] in ["ADT","JCB"]:
                    pax_type = f"""<PassengerType Code="JCB" Quantity="{pax["quantity"]}"/>"""
            
                elif pax['code'] in child_list:
                    code = "J"+str(pax['code'][-2:])
                    pax_type = "<PassengerType Code='"+code+ "' Quantity='" +pax['quantity'] + "'/>" 
                
                elif pax['code'] in ["INF","JNF"]:
                    pax_type = f"""<PassengerType Code="JNF" Quantity="{pax["quantity"]}"/>"""
                
            for j in pax['nameSelect']:
                name_select = "<NameSelect NameNumber='"+str(j)+"'/>" 
        return pax_type, name_select

    def _get_hemisphere_code(self, region_name):
    
        hemisphere_code = "0"

        if region_name == "United States":
            hemisphere_code = "0"
        
        if region_name == "Central America":
            hemisphere_code = "1"
        
        if region_name == "Caribbean":
            hemisphere_code = "2"
        
        if region_name == "Latin America":
            hemisphere_code = "3"

        if region_name == "Europe":
            hemisphere_code = "4"
        
        if region_name == "Africa":
            hemisphere_code = "5"
        
        if region_name == "Middle East":
            hemisphere_code = "6"
        
        if region_name == "Asia":
            hemisphere_code = "7"
        
        if region_name == "Asia Pacific":
            hemisphere_code = "8"
        
        if region_name == "Canada":
            hemisphere_code = "9"
            
        return hemisphere_code

    def _get_commision(self, baggage,pcc, region_name):

        hemisphere_code = self._get_hemisphere_code(region_name)
        commission = "<MiscQualifiers>"
        if baggage > 0:
            commission = commission+"<BaggageAllowance Number='"+str(baggage)+"'/>"
        if pcc == "3GAH":
            commission = commission+"<HemisphereCode>"+hemisphere_code+"</HemisphereCode>"
            commission = commission+"<JourneyCode>"+'2'+"</JourneyCode>"
        
        commission = commission+"</MiscQualifiers>"
        if commission == "<MiscQualifiers></MiscQualifiers>":
            commission = ""
        return commission


    def cancel_list_segment(self,token_session,list_segment):
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
        return self.xml_builder.cancel_segment_rq(token_session,list_segment)
    
    def search_flightrq(self,request_searh):
        """
        This function is for searching flight
        :return : available flight for the specific request_search
        """

        # test = SabreBFMBuilder(request_searh).search_flight()
        #print(test)
        pass
    
    def fop_choice(self, code_cc = None, expire_date = None, cc_number = None, approval_code = None, payment_type = None, commission_value = None):
        if code_cc and expire_date and cc_number is not None:
            fop = self.xml_builder.info_credit_card(code_cc, expire_date, cc_number, approval_code, commission_value)
        elif payment_type and commission_value is not None:     
            fop = self.xml_builder.info_cash_or_cheque(payment_type, commission_value)
        return fop
    
    def issue_ticket(self, token_value, price_quote, code_cc = None, expire_date = None, cc_number = None, approval_code = None, payment_type = None, commission_value = None):
        """
        This function is for issue ticket 
        :return 
        """
        fop_type = self.fop_choice(code_cc, expire_date, cc_number, approval_code, payment_type, commission_value)
        request_data = self.xml_builder.air_ticket_rq(token_value, fop_type, price_quote)
        response_data = self.__request_wrapper("air_ticket_rq", request_data, self.xml_builder.url)
        return IssueTicketExtractor(response_data).extract()

if __name__ == "__main__":
    SabreClient("oui","yes","ok",False).search_flightrq({'pcc':"yes"})

