# This file will be change for refactoring purpose.
# This file is for Sabre reservation classes and functions
# TODO: Use "import" statements for packages and modules only, not for individual classes or functions.
# Note that there is an explicit exemption for

import requests
import jxmlease
from pygds.core.client import BaseClient
from pygds.core.sessions import SessionInfo
from pygds.sabre.xmlbuilders.builder import SabreXMLBuilder
from pygds.sabre.helpers import get_data_from_json as from_json

from pygds.sabre.xml_parsers.response_extractor import PriceSearchExtractor
from pygds.sabre.hemisphere_code import get_hemisphere_code
from pygds.core.security_utils import generate_random_message_id
from pygds.errors.gdserrors import NoSessionError


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
        
    def search_price_quote(self, message_id, retain: bool=False, fare_type: str='', segment_select: list=[], passenger_type: list=[],baggage: int=0, pcc: str="", region_name: str=""):
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
        _, _, token_session = self.get_or_create_session_details(message_id)
        if token_session is None:
            raise NoSessionError(message_id)

        segment_number = self._get_segment_number(segment_select)
        fare_type_value = self._get_fare_type(fare_type) if self._get_fare_type(fare_type) else ""
        passenger_type, name_select = self._get_passenger_type(passenger_type, fare_type) 
        commission = self._get_commision(baggage, pcc, region_name)
        
        search_price_request = self.xml_builder.price_quote_rq(token_session,retain=str(retain).lower(), commission=commission, fare_type=fare_type_value, segment_select=segment_number, name_select=name_select, passenger_type=passenger_type)
        
        search_price_response = self.__request_wrapper("search_price_quote", search_price_request,
                                               self.xml_builder.url)
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
        pax_type = ""
        name_select = ""
        for pax in passenger_type:
            if fare_type == "Pub":
                if pax['code'] in ["ADT","JCB"]:
                    pax_type = pax_type+f"""<PassengerType Code="ADT" Quantity="{str(pax["quantity"])}"/>"""
                
                elif pax_type['code'] in child_list:
                    code = "C"+str(pax['code'][-2:])
                    pax_type = pax_type+"<PassengerType Code='"+code+ "' Quantity='" +str(pax['quantity']) + "'/>" 
                
                elif pax['code'] in ["INF","JNF"]:
                    pax_type = pax_type+f"""<PassengerType Code="INF" Quantity="{str(pax["quantity"])}"/>"""

            elif fare_type == "Net":
                if pax['code'] in ["ADT","JCB"]:
                    pax_type = pax_type+f"""<PassengerType Code="JCB" Quantity="{str(pax["quantity"])}"/>"""
            
                elif pax['code'] in child_list:
                    code = "J"+str(pax['code'][-2:])
                    pax_type = pax_type+"<PassengerType Code='"+code+ "' Quantity='" +str(pax['quantity']) + "'/>" 
                
                elif pax['code'] in ["INF","JNF"]:
                    pax_type = pax_type+f"""<PassengerType Code="JNF" Quantity="{str(pax["quantity"])}"/>"""
                
            for j in pax['nameSelect']:
                name_select = name_select+"<NameSelect NameNumber='"+str(j)+"'/>" 
        return pax_type, name_select

   

    def _get_commision(self, baggage,pcc, region_name):

        hemisphere_code = get_hemisphere_code(region_name)
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


if __name__ == "__main__":
    SabreClient("oui","yes","ok",False).search_flightrq({'pcc':"yes"})

