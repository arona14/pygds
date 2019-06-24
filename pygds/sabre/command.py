# This file will be change for refactoring purpose.

import requests

from pygds.sabre.helpers import soap_service_to_json
from pygds.sabre.base_service import BaseService
from pygds.sabre.session import SabreSession
from pygds.sabre.xmlbuilders.builder import SabreXMLBuilder


class SabreCommand(BaseService):
    """ this class contains all sabre command """

    def send(self, command, pcc, token=None, conversation_id=None):
        """ this method take a parameters: command name, pcc token, record locator, conversation_id
            and return the status of command """

        need_close = False
        if token is None:
            token = SabreSession().open(pcc, conversation_id)
            need_close = True

        command_xml = SabreXMLBuilder().sabreCommandLLSRQ(pcc, token, conversation_id, command)
        command_xml = command_xml.encode('utf-8')

        response = requests.post(self.url, data=command_xml, headers=self.headers)

        send_command = soap_service_to_json(response)

        if need_close:
            SabreSession().close(pcc, token, conversation_id)
        return send_command
