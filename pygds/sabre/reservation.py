# This file is for Sabre reservation classes and functions

import requests
import json
from .session import SabreSession
from .xmlbuilders.builder import SabreXMLBuilder
from .helper import fromSoapResponse

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
            toreturn_dict = fromSoapResponse(response)
            toreturn_dict = getReservationDataProcessing(response)
            if need_close:
                SabreSession().close(pcc, conversation_id, token_session)
        except:
            toreturn_dict = None
        return toreturn_dict


    def getReservationDataProcessing(response):
        """Get and Return Json dict."""
        dict_result=[]
        try:
            json_object = json.load(response)
            if json_object is not None:
                json_item_Passengers = (json_object['Reservation']['PassengerReservation']['Passengers']['Passenger'])
                json_item_Segments = (json_object['Reservation']['PassengerReservation']['Segments']['Segment'])
                json_item_FormsOfPayment = (json_object['Reservation']['PassengerReservation']['FormsOfPayment'])
                json_item_TicketingInfo = (json_object['Reservation']['PassengerReservation']['TicketingInfo'])
                json_item_PriceQuote = (json_object['PriceQuote'])
                json_item_Remark = (json_object['Reservation']['Remarks']['Remark'])

                dict_result.append(json_item_Segments)
                dict_result.append(json_item_Passengers)
                dict_result.append(json_item_PriceQuote)
                dict_result.append(json_item_TicketingInfo)
                dict_result.append(json_item_FormsOfPayment)
                dict_result.append(json_item_Remark)

                return dict_result
        except ValueError:
            dict_result = None
        return dict_result