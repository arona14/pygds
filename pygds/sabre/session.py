# This file will be change for refactoring purpose.
# TODO: Use "import" statements for packages and modules only, not for individual classes or functions.
# Note that there is an explicit exemption for

import requests
import jxmlease

from pygds.sabre.helpers import soap_service_to_json
from pygds.sabre.base_service import BaseService
from pygds.sabre.config import sabre_credentials, decode_base64
from pygds.sabre.xmlbuilders.builder import SabreXMLBuilder


class SabreSession(BaseService):

    def __init__(self, pcc, user_name, password, conversation_id, url, headers):
        self.pcc = pcc
        self.user_name = user_name
        self.password = password
        self.conversation_id = conversation_id
        self.url = url
        self.headers = headers

    def open(self):
        try:
            open_session_xml = SabreXMLBuilder().session_create_rq(
                self.pcc, self.user_name, self.password, self.conversation_id)

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


def main():
    pass


if __name__ == '__main__':
    main()
