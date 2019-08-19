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


class SabreClient(BaseClient):
    """
    A class to interact with Sabre GDS
    """
    def __init__(self, url: str, username: str, password: str, pcc: str, debug: bool = False):
        super().__init__(url, username, password, pcc, debug)
        self.xml_builder = SabreXMLBuilder(url, username, password, pcc)
        self.header_template = {'content-type': 'text/xml; charset=utf-8'}

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
        
    def search_price_quote(self, message_id, retain:bool=False, commission:float=0, tour_code:str='', fare_type:str='', ticket_designator:str='', segment_select:str='', name_select:str='', passenger_type:str='', plus_up:str='',baggage:str='', pcc:str="", hemisphere_code:str="", journey_code:str="", child_list:list =[]):
        """
        A method to cancel segment
        :param message_id: the message id 
        :return: None
        """
        _, _, token_session = self.get_or_create_session_details(message_id)
        session_info = None
        if not token_session:
            session_info = self.open_session()
            token_session = session_info.security_token

        segment_number = self._get_segment_number(segment_select)
        fare_type_value = self._get_fare_type(fare_type) if self._get_fare_type(fare_type) else ""
        passenger_type, name_select = self._get_passenger_type(passenger_type, fare_type, child_list) 
        commission = self._get_commision(commission, baggage, pcc, hemisphere_code, journey_code)

        search_price_quote = self.xml_builder.price_quote_rq(token_session,retain=retain,commission=commission,tour_code=tour_code,fare_type=fare_type_value,ticket_designator=ticket_designator,segment_select=segment_number,name_select=name_select,passenger_type=passenger_type,plus_up=plus_up) if retain else  self.xml_builder.price_quote_rq(token_session, retain, fare_type, segment_select=segment_select, name_select=name_select, passenger_type=passenger_type)
        
        response =  requests.post(self.xml_builder.url, data=search_price_quote, headers=self.header_template)
        return response.content

    def _get_segment_number(self, segment_select):
        if segment_select != []:
            segment_number = "<ItineraryOptions>"
            for k in segment_select:
                segment_number = segment_number+"<SegmentSelect Number='"+k+"'/>" 
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


    def _get_passenger_type(self, passenger_type, fare_type, child_list):

        for pax in passenger_type:
            if fare_type == "Pub":
                if pax_type['code'] in ["ADT","JCB"]:
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
                name_select = "<NameSelect NameNumber='"+j+"'/>" 
        return pax_type, name_select


    def _get_commision(self, commission, baggage,pcc, hemisphere_code, journey_code):

        commission = "<MiscQualifiers>"
        if baggage != "0":
            commission = commission+"<BaggageAllowance Number='"+str(baggage)+"'/>"
        if pcc == "3GAH":
            commission = commission+"<HemisphereCode>"+hemisphere_code+"</HemisphereCode>"
            commission = commission+"<JourneyCode>"+journey_code+"</JourneyCode>"
        
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

