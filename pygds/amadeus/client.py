from .xmlbuilders.builder import AmadeusXMLBuilder
from .env_settings import get_setting
import requests
import jxmlease


class AmadeusClient():
    """
        This is the main class to make calls to Amadeus API
    """
    def __init__(self):
        endpoint = get_setting("AMADEUS_ENDPOINT_URL")
        username = get_setting("AMADEUS_USERNAME")
        password = get_setting("AMADEUS_PASSWORD")
        office_id = get_setting("AMADEUS_OFFICE_ID")
        wsap = get_setting("AMADEUS_WSAP")
        self.endpoint = endpoint
        self.username = username
        self.password = password
        self.office_id = office_id
        self.xmlbuilder: AmadeusXMLBuilder = AmadeusXMLBuilder(endpoint, username, password, office_id, wsap)

    def start_new_session(self):
        request_data = self.xmlbuilder.start_transaction(None, self.office_id, self.username, self.password, None, None)
        print(request_data)
        headers = {'Content-Type': 'text/xml;charset=UTF-8', 'Accept-Encoding': 'gzip,deflate', 'SOAPAction': 'http://webservices.amadeus.com/VLSSOQ_04_1_1A'}
        response = requests.post(self.endpoint, data=request_data, headers=headers)
        response_data = jxmlease.parse(response.content)
        return response_data
