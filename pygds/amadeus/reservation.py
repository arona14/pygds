# This file will be change for refactoring purpose.
# This file is for Amadeus reservation classes and functions

import requests
from amadeus.session import AmadeusSession
from amadeus.xmlbuilders.builder import AmadeusXMLBuilder
from amadeus.helpers import FormatSoapAmadeus
from amadeus.base_service import BaseServiceAmadeus
from amadues.helpers import FormatSoapAmadeus

class AmadeusReservation(BaseServiceAmadeus):
    """This class contains all the services for manipulation a reservation."""

    def get(self, pnr, pcc, conversation_id, status_session):
        """Return the reservation data."""
        try:
            token_session = AmadeusSession().open(pcc, conversation_id)
            get_reservation = AmadeusXMLBuilder().getReservationRQ(pcc, conversation_id, token_session, record_locator, status_session)
            response = requests.post(self.url, data=get_reservation, headers=self.headers)
            to_return_dict = FormatSoapAmadeus().get_reservation_response(response)
        except:
            # TODO: Capture the real exception not the general one
            to_return_dict = None
        return to_return_dict
