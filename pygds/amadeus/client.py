from .xmlbuilders.builder import AmadeusXMLBuilder
import requests
import jxmlease


class AmadeusClient():
    """
        This is the main class to make calls to Amadeus API
    """
    def __init__(self, endpoint: str, username: str, password: str, office_id: str, wsap: str):
        self.endpoint = endpoint
        self.username = username
        self.password = password
        self.office_id = office_id
        self.xmlbuilder: AmadeusXMLBuilder = AmadeusXMLBuilder(endpoint, username, password, office_id, wsap)

    def start_new_session(self):
        request_data = self.xmlbuilder.start_transaction(None, self.office_id, self.username, self.password, None, None)
        headers = {'Content-Type': 'text/xml;charset=UTF-8', 'Accept-Encoding': 'gzip,deflate', 'SOAPAction': 'http://webservices.amadeus.com/VLSSOQ_04_1_1A'}
        response = requests.post(self.endpoint, data=request_data, headers=headers)
        status = response.status_code
        print(f"status: {status}")
        response_data = jxmlease.parse(response.content)
#        if status == 500:
#            # handle errors by building the correspondig Exception object
#            raise ValueError(f'Error with status {status}')
        return response_data
