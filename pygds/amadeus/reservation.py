# This file will be change for refactoring purpose.
# This file is for Amadeus reservation classes and functions

import requests
#from amadeus.session import AmadeusSession
from pygds.amadeus.xmlbuilders.builder import AmadeusXMLBuilder
from pygds.amadeus.base_service import BaseServiceAmadeus
from .helpers import FormatSoapAmadeus

class AmadeusReservation(BaseServiceAmadeus):
    """This class contains all the services for manipulation a reservation.token= 1ED1LY2NGF8EG3LTQIXYZ738HZ"""

    def get(self, pcc, conversation_id, status_session):
        """Return the reservation data."""
        try:
            token_session = "1ED1LY2NGF8EG3LTQIXYZ738HZ" #AmadeusSession().open(pcc, conversation_id)
            get_reservation = AmadeusXMLBuilder().getReservationRQ(pcc, conversation_id, token_session, record_locator, status_session)
            response = requests.post(self.url, data=get_reservation, headers=self.headers)
            to_return_dict = FormatSoapAmadeus().get_reservation_response(response)
        except:
            # TODO: Capture the real exception not the general one
            to_return_dict = None
        return to_return_dict
