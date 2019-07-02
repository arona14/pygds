# This file will be change for refactoring purpose.
# TODO: Use "import" statements for packages and modules only, not for individual classes or functions.
# Note that there is an explicit exemption for

import requests

from pygds.sabre.helpers import soap_service_to_json
from pygds.sabre.base_service import BaseService
from pygds.sabre.session import SabreSession
from pygds.sabre.xmlbuilders.builder import SabreXMLBuilder


class SabreCommand(BaseService):
    """ This class contains all sabre command """

    def send(self, command, pcc, token=None, conversation_id=None):
        """ This method take a parameters: command name, pcc token, record locator, conversation_id
            and return the status of command """

        need_close = False
        if token is None:
            token = SabreSession().open(pcc, conversation_id)
            need_close = True

        command_xml = SabreXMLBuilder().sabre_command_lls_rq(pcc, token, conversation_id, command)
        command_xml = command_xml.encode('utf-8')

        response = requests.post(self.url, data=command_xml, headers=self.headers)

        send_command = soap_service_to_json(response.content)

        if need_close:
            SabreSession().close(pcc, token, conversation_id)
        return send_command


def main():
    pass


if __name__ == '__main__':
    main()
