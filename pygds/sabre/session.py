# This file will be change for refactoring purpose.

import requests
import jxmlease

from pygds.sabre.helpers import soap_service_to_json
from pygds.sabre.base_service import BaseService
from pygds.sabre.config import sabre_credentials, decode_base64
from pygds.sabre.xmlbuilders.builder import SabreXMLBuilder


class SabreSession(BaseService):

    def open(self, pcc, conversation_id):

        sabre_credential = sabre_credentials(pcc)

        try:
            user_name = sabre_credential["User"][0]
            password = decode_base64(sabre_credential["Password1"][0])

            open_session_xml = SabreXMLBuilder().session_create_rq(
                pcc, user_name, password, conversation_id)

            response = requests.post(self.url, data=open_session_xml, headers=self.headers)
            r = jxmlease.parse(response.content)
            token = r[u'soap-env:Envelope'][u'soap-env:Header'][u'wsse:Security'][u'wsse:BinarySecurityToken']

        except:
            # TODO: Capture the real exception not the general one
            token = None
        return token

    def close(self, pcc, token, conversation_id):

        close_session_xml = SabreXMLBuilder().session_close_rq(pcc, token, conversation_id)

        response = requests.post(self.url, data=close_session_xml, headers=self.headers)
        return soap_service_to_json(response.content)
