import requests

from pygds.sabre.base_service import BaseService
from pygds.sabre.session import SabreSession
from pygds.sabre.xmlbuilders.builder import SabreXMLBuilder
from pygds.sabre.helpers import soap_service_to_json


class SabreClient(BaseService):
    # def __init__(self):
    #     pass

    def open_session(self, pcc, conversation_id):
        """
        This will open a new session
        :param pcc: The PCC
        :param conversation_id: the conversion id
        :return: a token session
        """
        SabreSession().open(pcc, conversation_id)

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
