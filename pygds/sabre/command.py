from .xmlbuilders.builder import SabreXMLBuilder
from .session import SabreSession
import requests,json,xmltodict

class SabreCommand :
    """ this class contains all sabre commande """

    def __init__(self):
        self.url  = "https://webservices3.sabre.com"
        self.headers = {'content-type': 'text/xml'}
    
    def send(self, command, pcc, token = None, conversation_id = None) :

        """ this method take a parameters: command name, pcc token,recordlocator,conversation_id 
            and return the status of command """
        if token == None :
                token = SabreSession().open(pcc,conversation_id)
                need_close = True
        command_xml = SabreXMLBuilder().sabreCommandLLSRQ(pcc,token,conversation_id,command)
        command_xml = command_xml.encode('utf-8')
        response = requests.post(self.url, data=command_xml, headers=self.headers)
        send_command = json.loads(json.dumps(xmltodict.parse(response.content)))
        send_command = str(send_command).replace("@","")
        send_command = send_command.replace("u'","'") 
        send_command = eval(send_command)
        if need_close :
            SabreSession().close(pcc, token, conversation_id)
        return send_command 