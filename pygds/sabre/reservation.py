# This file will be change for refactoring purpose.
# This file is for Sabre reservation classes and functions
# TODO: Use "import" statements for packages and modules only, not for individual classes or functions.
# Note that there is an explicit exemption for

import requests

from pygds.sabre.base_service import BaseService
from pygds.sabre.session import SabreSession
from pygds.sabre.xmlbuilders.builder import SabreXMLBuilder
from pygds.sabre.helpers import soap_service_to_json


def reformat_sabre_get_reservation(data):
    """
    Transform a raw json sabre response and transform it to custom dict.

    :param data: raw sabre response (dict/json)
    :return: {dict}
    """
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
    """This class contains all the services for manipulation a reservation.
    """
    def get(self, pnr: str, pcc: str, conversation_id: str, need_close=True):
        """
        Returns the Sabre reservation data
        :param pnr: the record locator of the reservation
        :param pcc: Pseudo City Code or OfficeId
        :param conversation_id: the conversation identifier
        :param need_close: will allow the method to know if it will close the session
        :return: {dict}
        """
        try:
            token_session = SabreSession().open(pcc, conversation_id)
            get_reservation = SabreXMLBuilder().get_reservation_rq(pcc, conversation_id, token_session, pnr)
            response = requests.post(self.url, data=get_reservation, headers=self.headers)
            to_return = soap_service_to_json(response.content)
            to_return_dict = reformat_sabre_get_reservation(to_return)
            if need_close:
                SabreSession().close(pcc, conversation_id, token_session)
        except:
            # TODO: Capture the real exception not the general one
            to_return_dict = None
        return to_return_dict
