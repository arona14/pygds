import json
import requests
import xmltodict

from .xmlbuilders.builder import SabreXMLBuilder


class SabreTransaction:

    def __init__(self):
        self.url = "https://webservices3.sabre.com"
        self.headers = {'content-type': 'text/xml'}

    def end(self, pcc, token, conversation_id):

        """End Transaction method"""

        end_transaction_xml = SabreXMLBuilder().endTransactionRQ(pcc, token, conversation_id)
        response = requests.post(self.url, data=end_transaction_xml, headers=self.headers)
        end_transaction = json.loads(json.dumps(xmltodict.parse(response.content)))
        end_transaction = str(end_transaction).replace("@", "")
        end_transaction = end_transaction.replace("u'", "'")
        end_transaction = eval(end_transaction)

        if end_transaction['soap-env:Envelope']['soap-env:Body']['EndTransactionRS']['stl:ApplicationResults']['status'] != "Complete":
            end_transaction_xml = SabreXMLBuilder().endTransactionRQ(pcc, token, conversation_id)
            response = requests.post(self.url, data=end_transaction_xml, headers=self.headers)
            end_transaction = json.loads(json.dumps(xmltodict.parse(response.content)))
            end_transaction = str(end_transaction).replace("@", "")
            end_transaction = end_transaction.replace("u'", "'")
            end_transaction = eval(end_transaction)

        return end_transaction["soap-env:Envelope"]["soap-env:Body"]

    def ignore(self):
        pass
