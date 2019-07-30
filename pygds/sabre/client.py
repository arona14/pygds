import requests

from pygds.core.client import BaseClient
from pygds.sabre.session import SabreSession
from pygds.sabre.xmlbuilders.builder import SabreXMLBuilder
from pygds.sabre.helpers import soap_service_to_json
from pygds.sabre.jsonbuilders.builder import  SabreBFMBuilder

from pygds.core.request import  LowFareSearchRequest



class SabreClient(BaseClient):
    """
    A class to interact with Sabre GDS
    """
    def __init__(self, url: str, username: str, password: str, pcc: str, debug: bool = False):
        super().__init__(url, username, password, pcc, debug)
        self.xml_builder = SabreXMLBuilder(url, username, password, pcc)
        self.header_template = {'content-type': 'text/xml; charset=utf-8'}

    def open_session(self):
        """
        This will open a new session
        :return: a token session
        """
        open_session_xml = self.xml_builder.session_create_rq()
        response = self._request_wrapper(open_session_xml, None)
        return response.content

        # r = jxmlease.parse(response.content)
        # token = r[u'soap-env:Envelope'][u'soap-env:Header'][u'wsse:Security'][u'wsse:BinarySecurityToken']

    def close_session(self, pcc, conversation_id, token_session):
        """
        A method to close a session
        :param pcc: The PCC
        :param conversation_id: the conversation id
        :param token_session: the token session
        :return: None
        """
        SabreSession().close(pcc, conversation_id, token_session)

    def get_reservation(self, pnr: str, pcc: str, conversation_id: str, need_close=True):
        """
        retrieve PNR
        :param pnr: the record locator
        :param pcc: the PCC
        :param conversation_id: The conversation id
        :param need_close: close or not the session
        :return: a Reservation object
        """
        try:
            token_session = self.open_session(pcc, conversation_id)

            get_reservation = SabreXMLBuilder().get_reservation_rq(pcc, conversation_id, token_session, pnr)
            response = requests.post(self.url, data=get_reservation, headers=self.headers)

            to_return = soap_service_to_json(response.content)
            to_return_dict = to_return

            if need_close:
                self.close_session(pcc, conversation_id, token_session)
        except:
            # TODO: Capture the real exception not the general one
            to_return_dict = None
        return to_return_dict

    def search_flightrq(self,request_searh):
        """
        This function is for searching flight
        :return : available flight for the specific request_search
        """

        test = SabreBFMBuilder(request_searh).search_flight()
        #print(test)


if __name__ == "__main__":
    SabreClient("oui","yes","ok",False).search_flightrq({'pcc':"yes"})

