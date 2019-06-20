# This file is for Sabre reservation classes and functions

import requests
import json
from .session import SabreSession
from .xmlbuilders.builder import SabreXMLBuilder
from .helpers import fromSoapResponse

class SabreReservation:
    """This class contains all the services for manupilation a reservation."""

    def __init__(self):
        self.url = "https://webservices3.sabre.com"
        self.headers = {'content-type': 'text/xml'}

    def get(self, pnr, pcc, conversation_id, need_close = True):
        """Return the reservation data."""
        try:
            token_session = SabreSession().open(pcc, conversation_id)
            get_reservation = SabreXMLBuilder().getReservationRQ(pcc, conversation_id, token_session, pnr)
            response = requests.post(self.url, data=get_reservation, headers=self.headers)
            toreturn = fromSoapResponse(response)
            toreturn_dict = self.getReservationDataProcessing(toreturn)
            if need_close:
                SabreSession().close(pcc, conversation_id, token_session)
        except:
            toreturn_dict = None
        return toreturn_dict


    def getReservationDataProcessing(self,response):
        """Get and Return Json dict."""
        dict_result= []
        try:
            json_item_Passengers = response.get('Passenger')
            json_item_Segments = response.get('Segment')
            json_item_FormsOfPayment = response.get('FormsOfPayment')
            json_item_TicketingInfo = response.get('TicketingInfo')
            json_item_Remark = response.get('Remark')
            json_item_PriceQuote = response.get('PriceQuote')

            dict_result.append(json_item_Segments)
            dict_result.append(json_item_Passengers)
            dict_result.append(json_item_Remark)
            dict_result.append(json_item_PriceQuote)
            dict_result.append(json_item_TicketingInfo)
            dict_result.append(json_item_FormsOfPayment)
            return dict_result
        except:
            dict_result = None
        return dict_result