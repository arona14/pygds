# This file is for Sabre reservation classes and functions

import requests

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
            if need_close:
                SabreSession().close(pcc, conversation_id, token_session)
        except:
            toreturn_dict = None
        return toreturn_dict
