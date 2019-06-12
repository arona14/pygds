from .xmlbuilders.builder import SabreXMLBuilder
import requests

class SabreCommand :
    """ this class contains all sabre commande """

    def __init__(self):
        self.url  = "https://webservices3.sabre.com"
        self.headers = {'content-type': 'text/xml'}
    
    def send(self, command, pcc, token = None, conversation_id = None) :

        """ this method take a parameters: command name, pcc token,recordlocator,conversation_id 
            and return the status of command """

        command_xml = SabreXMLBuilder().sabreCommandLLSRQ(pcc,token,conversation_id,command)
        command_xml = command_xml.encode('utf-8')
        response = requests.post(self.url, data=command_xml, headers=self.headers)
        return response.content 