# This file will be change for refactoring purpose.
# This file is for Amadeus reservation classes and functions
import requests
from .xmlbuilders.builder import AmadeusXMLBuilder
from .helpers import FormatSoapAmadeus
from ..env_settings import get_setting


class AmadeusReservation:
    """The class contains the functions that make getReservation for example the get function which is responsible for sending us a pnr"""

    def get(self, pcc, conversation_id, status_session):
        """Return the reservation data."""
        url = "https://nodeD1.test.webservices.amadeus.com"
        header = {'Content-Type': 'text/xml;charset=UTF-8', 'Accept-Encoding': 'gzip,deflate', 'SOAPAction': 'http://webservices.amadeus.com/PNRRET_17_1_1A'}
        endpoint = get_setting("AMADEUS_ENDPOINT_URL")
        username = get_setting("AMADEUS_USERNAME")
        password = get_setting("AMADEUS_PASSWORD")
        office_id = "DTW1S210B"
        wsap = get_setting("AMADEUS_WSAP")
        record_locator = "RLIQBP"
        Token_session = "3NW981XMP9CCJ2WBTJMC7R0DHW"
        try:
            token_session = Token_session
            get_reservation = AmadeusXMLBuilder(endpoint, username, password, office_id, wsap).get_reservation_builder(pcc, conversation_id, token_session, record_locator, status_session)
            response = requests.post(url, data=get_reservation, headers=header)
            to_return_dict = FormatSoapAmadeus().get_reservation_response(response.content)
        except Exception as e:
            print(e)
            # TODO: Capture the real exception not the general one
            to_return_dict = None
            raise e
        return to_return_dict


def test():
    """
        This is just for testing and needs to be removed after
    """
    office_id = get_setting("AMADEUS_OFFICE_ID")
    pnr = "QK2W23"
    status_session = True
    print(AmadeusReservation().get(office_id, pnr, status_session))


if __name__ == "__main__":
    test()
