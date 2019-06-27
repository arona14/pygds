# This file will be change for refactoring purpose.

import requests

from pygds.sabre.helpers import soap_service_to_json
from pygds.sabre.base_service import BaseService
from pygds.sabre.xmlbuilders.builder import SabreXMLBuilder


class SabreTransaction(BaseService):

    def end(self, pcc, token, conversation_id):
        """End Transaction method"""

        end_transaction_xml = SabreXMLBuilder().end_transaction_rq(pcc, token, conversation_id)
        response = requests.post(self.url, data=end_transaction_xml, headers=self.headers)
        return soap_service_to_json(response)  # TODO: Need to check the complete status and send a second one if needed

    def ignore(self):
        pass
