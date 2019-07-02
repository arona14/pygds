# This file will be change for refactoring purpose.
# This file is for Amadeus reservation classes and functions
import requests
from xmlbuilders.builder import AmadeusXMLBuilder
#from amadeus.base_service import BaseServiceAmadeus
#from amadeus.helpers import FormatSoapAmadeus 
from env_settings_ import get_setting


class AmadeusReservation():
    """This class contains all the services for manipulation a reservation.token= 1ED1LY2NGF8EG3LTQIXYZ738HZ"""

    def get(self, pcc, conversation_id, status_session):
        """Return the reservation data."""
        url = "https://nodeD1.test.webservices.amadeus.com"
        header ={'Content-Type': 'text/xml;charset=UTF-8', 'Accept-Encoding': 'gzip,deflate', 'SOAPAction': 'http://webservices.amadeus.com/PNRRET_17_1_1A'}
        endpoint = get_setting("AMADEUS_ENDPOINT_URL")
        username = get_setting("AMADEUS_USERNAME")
        password = get_setting("AMADEUS_PASSWORD")
        office_id = "DTW1S210B"#get_setting("AMADEUS_OFFICE_ID")
        wsap = get_setting("AMADEUS_WSAP")
        record_locator = "RLIQBP"
        try:
            token_session = "26K97CWQWTL9F1PP67LMZHJSXC" #AmadeusSession().open(pcc, conversation_id)
            get_reservation = AmadeusXMLBuilder(endpoint, username, password, office_id, wsap).getReservationRQ(pcc, conversation_id, token_session, record_locator, status_session)
            #print(get_reservation)
            response = requests.post(url, data=get_reservation, headers=header)
            to_return_dict = response.content #FormatSoapAmadeus().get_reservation_response(response)
        except Exception as e:
            print(e)
            # TODO: Capture the real exception not the general one
            to_return_dict = None
            raise e
        return to_return_dict



office_id = get_setting("AMADEUS_OFFICE_ID")
pnr= "QK2W23"
status_session = True
print(AmadeusReservation().get(office_id, pnr, status_session))
