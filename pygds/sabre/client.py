import requests

from pygds.sabre.base_service import BaseService
from pygds.sabre.session import SabreSession
from pygds.sabre.xmlbuilders.builder import SabreXMLBuilder
from pygds.sabre.helpers import soap_service_to_json


class SabreClient(BaseService):
    # def __init__(self):
    #     pass

    def open_session(self, pcc, conversation_id):
        SabreSession().open(pcc, conversation_id)

    def close_session(self, pcc, conversation_id, token_session):
        SabreSession().close(pcc, conversation_id, token_session)

    def get_reservation(self, pnr: str, pcc: str, conversation_id: str, need_close=True):
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
    