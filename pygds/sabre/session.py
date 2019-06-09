import requests, jxmlease, json, xmltodict
from pygds.sabre.config import sabrecredential, base64ToString
from pygds.sabre.xmlbuilders.builder import SabreXMLBuilder

url = "https://webservices3.sabre.com"
headers = {'content-type': 'text/xml'}

class SabreSession():

    def open(pcc, conversation_id):

        sabre_credential = sabrecredential(pcc)

        try:
            user_name = sabre_credential["User"][0]
            password = base64ToString(sabre_credential["Password1"][0])

            open_session_xml = SabreXMLBuilder().sessionCreateRQ(pcc, user_name, password, conversation_id)

            response = requests.post(url, data=open_session_xml, headers=headers)
            r = jxmlease.parse(response.content)
            token = r[u'soap-env:Envelope'][u'soap-env:Header'][u'wsse:Security'][u'wsse:BinarySecurityToken']
        except:
            token = None
        return token

    def close(pcc, token, conversation_id):

        close_session_xml = SabreXMLBuilder().sessionCloseRQ(pcc, token, conversation_id)

        response = requests.post(url, data=close_session_xml, headers=headers)
        return json.loads(json.dumps(xmltodict.parse(response.content)))
