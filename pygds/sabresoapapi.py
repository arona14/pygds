
import requests,jxmlease,json,xmltodict
from pygds.config import sabrecredential,base64ToString,b64

class _Sabresoapapi():

    def __init__(self,gds):
        self._gds=gds
        self.url = "https://webservices3.sabre.com"
        self.headers = {'content-type': 'text/xml'}

    def tokensession(self,pcc=None,conversation_id=None):
    
        token_xml = self._gds.objectxml.sabretokensession(pcc,conversation_id)
        response = requests.post(self.url, data=token_xml, headers=self.headers)
        r = jxmlease.parse(response.content)
        try:
            token = r[u'soap-env:Envelope'][u'soap-env:Header'][u'wsse:Security'][u'wsse:BinarySecurityToken']
        except:
            token = None
        return token
    
    def authenticationTokenSessionLess(self,pcc=None):

        sabre_credential = sabrecredential(pcc)
        user_name = sabre_credential["User"][0]
        password = base64ToString(sabre_credential["Password1"][0])
        domain = "AA"
        format_version = "V1"
        credentials = f"""{format_version}:{user_name}:{pcc}:{domain}"""
        secret = b64(password)
        return b64(b64(credentials) + ":" + secret)
       
    def tokensessionless(self,pcc=None):
        
        authentication = self.authenticationTokenSessionLess(pcc=pcc)

        headers = {
            'Authorization' : "Basic " +str(authentication),
            'Accept' : '*/*'
        }
        environment = "https://api.havail.sabre.com"
        response = requests.post(environment+"/v2/auth/token", headers=headers, data={"grant_type" : "client_credentials"})
        to_return = json.loads(response.text)

        return    to_return
    
    def displaypnr(self,pcc=None,conversation_id=None,pnr=None):

        toreturn_dict = {}
        token_session = self.tokensession(pcc=pcc,conversation_id=conversation_id)
        get_reservation_xml = self._gds.objectxml.sabredisplaypnr(pcc=pcc,conversation_id=conversation_id,pnr=pnr,token=token_session)
        
        response = requests.post(self.url, data=get_reservation_xml, headers=self.headers)
        get_reservation = json.loads(json.dumps(xmltodict.parse(response.content)))
        toreturn_reservation  = get_reservation["soap-env:Envelope"]["soap-env:Body"]["stl18:GetReservationRS"]
        toreturn_reservation = str(toreturn_reservation).replace("@","")
        toreturn_dict = eval(toreturn_reservation.replace("u'","'"))
        toreturn_dict["Token"] = token_session
        toreturn_dict["ConversationId"] = conversation_id
        del toreturn_dict["xmlns:stl18"]
        del toreturn_dict["xmlns:ns6"]
        del toreturn_dict["xmlns:raw"]
        del toreturn_dict["xmlns:ns4"]
        del toreturn_dict["xmlns:or112"]
        return toreturn_dict
    
    def closesession(self,pcc = None,conversation_id = None,token = None):

        close_session = self._gds.objectxml.sabreclosesession(pcc=pcc,conversation_id=conversation_id,token=token)
        
        response = requests.post(self.url, data=close_session, headers=self.headers)
        toreturn = json.loads(json.dumps(xmltodict.parse(response.content)))
        
        return toreturn
    
    def endtransaction(self,pcc = None,conversation_id = None,token = None):

        end_transaction = self._gds.objectxml.sabreendtransaction(pcc=pcc,conversation_id=conversation_id,token=token)
        
        response = requests.post(self.url, data=end_transaction, headers=self.headers)
        toreturn = json.loads(json.dumps(xmltodict.parse(response.content)))
        
        return toreturn
    
    def sendcommand(self,pcc = None,conversation_id = None,token = None,command =None):

        send_command = self._gds.objectxml.sabresendcommand(pcc=pcc,conversation_id=conversation_id,token=token,command=command)
        response = requests.post(self.url, data=send_command, headers=self.headers)
        xml_dict_send_command = json.loads(json.dumps(xmltodict.parse(response.content)))
        toreturn = xml_dict_send_command
        toreturn = str(toreturn).replace("@","")
        toreturn = toreturn.replace("u'","'") 
        toreturn = eval(toreturn)
        
        return toreturn