# This file is for Sabre reservation classes and functions

import json
import requests
import xmltodict

from .session import SabreSession
from .xmlbuilders.builder import SabreXMLBuilder


class SabreReservation:
    """This class contains all the services for manupilation a reservation."""

    def __init__(self):
        self.url = "https://webservices3.sabre.com"
        self.headers = {'content-type': 'text/xml'}

    def get(self, pnr, pcc, conversation_id, need_close = True):
        """Return the reservation data."""

        toreturn_dict = {}

        token_session = SabreSession().open(pcc, conversation_id)
        get_reservation = SabreXMLBuilder().getReservationRQ(pcc, conversation_id, token_session, pnr)
        response = requests.post(self.url, data=get_reservation, headers=self.headers)
        get_reservation = json.loads(json.dumps(xmltodict.parse(response.content)))

        toreturn_reservation = get_reservation["soap-env:Envelope"]["soap-env:Body"]["stl19:GetReservationRS"]
        toreturn_reservation = str(toreturn_reservation).replace("@", "")
        toreturn_dict = eval(toreturn_reservation.replace("u'", "'"))

        if need_close:
            SabreSession().close(pcc, conversation_id, token_session)

        del toreturn_dict["xmlns:stl19"]
        del toreturn_dict["xmlns:ns6"]
        del toreturn_dict["xmlns:or114"]
        del toreturn_dict["xmlns:raw"]
        del toreturn_dict["xmlns:ns4"]

        return toreturn_dict
