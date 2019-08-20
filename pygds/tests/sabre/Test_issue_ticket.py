# from pygds.sabre.helpers import get_current_timestamp

def __init__(self):
    self.current_timestamp = str(strftime("%Y-%m-%dT%H:%M:%S",gmtime())) #get_current_timestamp()
    self.pcc = "WR17"
    self.conversation_id = "cosmo-material-b6851be0-b83e-11e8-be20-c56b920f05b5"
    self.token = ""
    self.code_cc = "" 
    self.expire_date = ""
    self.cc_number = ""
    self.approval_code = ""
    self.commission_value = ""
    self.price_quote = ""
    self.payment_type = "CS"
    self.type_fop_by_credit_card = SabreXMLBuilder().info_credit_card(self.code_cc, self.expire_date, self.cc_number, self.approval_code, self.commission_value)
    self.type_fop_by_cash_or_cheque =  SabreXMLBuilder().info_cash_or_cheque(self.payment_type, self.commission_value)

def generate_header(pcc, conversation_id, security_token):
    """
    This method generates the security part in SAOP Header.
    :param pcc: The pcc
    :param conversation_id: 
    :param security_token:
    :return:
    """
    return f"""<soapenv:Header>
                        <eb:MessageHeader xmlns:eb="http://www.ebxml.org/namespaces/messageHeader" soapenv:mustUnderstand="0">
                            <eb:From>
                                <eb:PartyId>sample.url.of.sabre.client.com</eb:PartyId>
                            </eb:From>
                            <eb:To>
                                <eb:PartyId>webservices.sabre.com</eb:PartyId>
                            </eb:To>
                            <eb:CPAId>{pcc}</eb:CPAId>
                            <eb:ConversationId>{conversation_id}</eb:ConversationId>
                            <eb:Service>AirTicketLLSRQ</eb:Service>
                            <eb:Action>AirTicketLLSRQ</eb:Action>
                            <eb:MessageData>
                                <eb:MessageId>mid:20001209-133003-2333@clientofsabre.com</eb:MessageId>
                                <eb:Timestamp>{current_timestamp}</eb:Timestamp>
                            </eb:MessageData>
                            <Description>CTS-PORTAL</Description>
                        </eb:MessageHeader>
                        <eb:Security xmlns:eb="http://schemas.xmlsoap.org/ws/2002/12/secext" soapenv:mustUnderstand="0">
                        <eb:BinarySecurityToken>{security_token}</eb:BinarySecurityToken>
                        <eb:group>{pcc}</eb:group>
                        </eb:Security>
                    </soapenv:Header>"""



def info_cash_or_cheque(payment_type, commission_value):
    return f"""<FOP_Qualifiers>
                <BasicFOP Type="{payment_type}"/>
                </FOP_Qualifiers>
                {commission_value}"""

def issue_air_ticket_soap(pcc, conversation_id, token_value, type_fop, price_quote):
    return  f"""<?xml version="1.0" encoding="UTF-8"?>
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
                <soapenv:Header>
                    <eb:MessageHeader xmlns:eb="http://www.ebxml.org/namespaces/messageHeader" soapenv:mustUnderstand="0">
                        <eb:From>
                            <eb:PartyId>sample.url.of.sabre.client.com</eb:PartyId>
                        </eb:From>
                        <eb:To>
                            <eb:PartyId>webservices.sabre.com</eb:PartyId>
                        </eb:To>
                        <eb:CPAId>{pcc}</eb:CPAId>
                        <eb:ConversationId>{conversation_id}</eb:ConversationId>
                        <eb:Service>AirTicketLLSRQ</eb:Service>
                        <eb:Action>AirTicketLLSRQ</eb:Action>
                        <eb:MessageData>
                            <eb:MessageId>mid:20001209-133003-2333@clientofsabre.com</eb:MessageId>
                            <eb:Timestamp>{current_timestamp}</eb:Timestamp>
                        </eb:MessageData>
                        <Description>CTS-PORTAL</Description>
                    </eb:MessageHeader>
                    <eb:Security xmlns:eb="http://schemas.xmlsoap.org/ws/2002/12/secext" soapenv:mustUnderstand="0">
                    <eb:BinarySecurityToken>{token_value}</eb:BinarySecurityToken>
                    <eb:group>{pcc}</eb:group>
                    </eb:Security>
                </soapenv:Header>
                    <soapenv:Body>
                        <AirTicketRQ Version="2.12.0" xmlns="http://webservices.sabre.com/sabreXML/2011/10" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" NumResponses="1" ReturnHostCommand="true">
                        <OptionalQualifiers>
                            {type_fop}
                            {price_quote}
                        </OptionalQualifiers>
                        </AirTicketRQ>
                    </soapenv:Body>
                </soapenv:Envelope>"""
    # body = issue_ticket_xml.encode(encoding='UTF-8')
    # return issue_ticket_xml

from time import gmtime, strftime
import requests
pcc = "WR17"
conversation_id = "cosmo-material-b6851be0-b83e-11e8-be20-c56b920f05b5"
payment_type = "CS"
commission_value = 100
type_fop = info_cash_or_cheque(payment_type, commission_value)
price_quote = 1234
token_value = "Shared/IDL:IceSess\\/SessMgr:1\\.0.IDL/Common/!ICESMS\\/RESH!ICESMSLB\\/RES.LB!-2983035619056495227!2255!0"
current_timestamp = str(strftime("%Y-%m-%dT%H:%M:%S",gmtime()))
url = "https://webservices3.sabre.com"
headers = {'content-type': 'text/xml; charset=utf-8'}
seat_map_xml = issue_air_ticket_soap(pcc, conversation_id, token_value, type_fop, price_quote)
response = requests.post(url, data=seat_map_xml, headers=headers)
print(response.content)