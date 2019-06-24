# This file will be change for refactoring purpose.
# This file is for Sabre reservation classes and functions

import requests

from .base_service import BaseService
from .session import SabreSession
from .xmlbuilders.builder import SabreXMLBuilder
from .helpers import soap_service_to_json


def reformat_sabre_get_reservation(data):
    """Get and Return Json dict."""

    print(data)
    dict_result = {}
    try:
        itineraries = []
        passengers = []
        form_of_payments = []
        price_quotes = []
        ticketing_info = []
        remarks = []

        dict_result['Itineraries'] = itineraries
        dict_result['Passengers'] = passengers
        dict_result['FormOfPayments'] = form_of_payments
        dict_result['PriceQuotes'] = price_quotes
        dict_result['TicketingInfo'] = ticketing_info
        dict_result['Remarks'] = remarks

        return dict_result
    except:
        # TODO: Capture the real exception not the general one
        dict_result = None
    return dict_result


class SabreReservation(BaseService):
    """This class contains all the services for manipulation a reservation."""

    def get(self, pnr, pcc, conversation_id, need_close=True):
        """Return the reservation data."""

        try:
            token_session = SabreSession().open(pcc, conversation_id)
            get_reservation = SabreXMLBuilder().getReservationRQ(pcc, conversation_id, token_session, pnr)
            response = requests.post(self.url, data=get_reservation, headers=self.headers)
            to_return = soap_service_to_json(response)
            to_return_dict = reformat_sabre_get_reservation(to_return)

            if need_close:
                SabreSession().close(pcc, conversation_id, token_session)
        except:
            # TODO: Capture the real exception not the general one
            to_return_dict = None

        return to_return_dict
