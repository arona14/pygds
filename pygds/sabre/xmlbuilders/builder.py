from time import gmtime, strftime


class SabreXMLBuilder:
    """This class can generate XML needed for sabre soap requests."""

    def __init__(self) :
        self.current_timestamp =  str(strftime("%Y-%m-%dT%H:%M:%S",gmtime()))

    def sessionCreateRQ(self, pcc, user_name, password, conversation_id):
        """Return the xml request to create a session."""


        return f"""<?xml version="1.0" encoding="UTF-8"?>
            <soap-env:Envelope xmlns:soap-env="http://schemas.xmlsoap.org/soap/envelope/" xmlns:eb="http://www.ebxml.org/namespaces/messageHeader" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsd="http://www.w3.org/1999/XMLSchema">
                <soap-env:Header>
                    <eb:MessageHeader soap-env:mustUnderstand="1" eb:version="1.0">
                        <eb:From>
                            <eb:PartyId />
                        </eb:From>
                        <eb:To>
                            <eb:PartyId />
                        </eb:To>
                        <eb:CPAId>{pcc}</eb:CPAId>
                        <eb:ConversationId>{conversation_id}</eb:ConversationId>
                        <eb:Service>SessionCreateRQ</eb:Service>
                        <eb:Action>SessionCreateRQ</eb:Action>
                        <eb:MessageData>
                            <eb:MessageId>mid:20001209-133003-2333@clientofsabre.com</eb:MessageId>
                            <eb:Timestamp>{self.current_timestamp}Z</eb:Timestamp>
                        </eb:MessageData>
                    </eb:MessageHeader>
                    <wsse:Security xmlns:wsse="http://schemas.xmlsoap.org/ws/2002/12/secext" xmlns:wsu="http://schemas.xmlsoap.org/ws/2002/12/utility">
                        <wsse:UsernameToken>
                            <wsse:Username>{user_name}</wsse:Username>
                            <wsse:Password>{password}</wsse:Password>
                            <Organization>{pcc}</Organization>
                            <Domain>DEFAULT</Domain>
                        </wsse:UsernameToken>
                    </wsse:Security>
                </soap-env:Header>
                <soap-env:Body>
                    <eb:Manifest soap-env:mustUnderstand="1" eb:version="1.0">
                        <eb:Reference xlink:href="cid:rootelement" xlink:type="simple" />
                    </eb:Manifest>
                    <SessionCreateRQ>
                        <POS>
                            <Source PseudoCityCode="{pcc}"/>
                        </POS>
                    </SessionCreateRQ>
                    <ns:SessionCreateRQ xmlns:ns="http://www.opentravel.org/OTA/2002/11" />
                </soap-env:Body>
            </soap-env:Envelope>"""

    def sessionCloseRQ(self, pcc, token, conversation_id):
        """Return the xml request to close a session."""

        return f"""<?xml version="1.0" encoding="UTF-8"?>
            <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
                <SOAP-ENV:Header>
                        <ns3:MessageHeader xmlns:ns2="http://www.w3.org/2000/09/xmldsig#"
                        xmlns:ns3="http://www.ebxml.org/namespaces/messageHeader"
                        xmlns:ns4="http://www.w3.org/1999/xlink"
                        xmlns:ns5="http://schemas.xmlsoap.org/ws/2002/12/secext">
                            <ns3:From>
                        <ns3:PartyId>sample.url.of.sabre.client.com</ns3:PartyId>
                            </ns3:From>
                            <ns3:To>
                        <ns3:PartyId>webservices.sabre.com</ns3:PartyId>
                            </ns3:To>
                            <ns3:CPAId>{pcc}</ns3:CPAId>
                        <ns3:ConversationId>{conversation_id}</ns3:ConversationId>
                            <ns3:Service>SessionCloseRQ</ns3:Service>
                            <ns3:Action>SessionCloseRQ</ns3:Action>
                            </ns3:MessageHeader>
                        <ns5:Security xmlns:ns2="http://www.w3.org/2000/09/xmldsig#"
                            xmlns:ns3="http://www.ebxml.org/namespaces/messageHeader"
                            xmlns:ns4="http://www.w3.org/1999/xlink"
                                xmlns:ns5="http://schemas.xmlsoap.org/ws/2002/12/secext">
                        <ns5:BinarySecurityToken>{token}</ns5:BinarySecurityToken>
                        <ns2:group>{pcc}</ns2:group>
                        </ns5:Security>
                </SOAP-ENV:Header>
                <SOAP-ENV:Body>
                    <SessionCloseRQ status="Approved" version="1" xmlns="http://www.opentravel.org/OTA/2002/11"/>
                </SOAP-ENV:Body>
            </SOAP-ENV:Envelope>"""

    def endTransactionRQ(self, pcc, token, conversation_id):

        current_timestamp = str(strftime("%Y-%m-%dT%H:%M:%S",gmtime()))

        return f"""<?xml version="1.0" encoding="UTF-8"?>
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
                <soapenv:Header>
                    <eb:MessageHeader xmlns:eb="http://www.ebxml.org/namespaces/messageHeader" soapenv:mustUnderstand="0">
                    <eb:From>
                        <eb:PartyId />
                    </eb:From>
                    <eb:To>
                        <eb:PartyId />
                    </eb:To>
                    <eb:CPAId>{pcc}</eb:CPAId>
                    <eb:ConversationId>{conversation_id}</eb:ConversationId>
                    <eb:Service>EndTransactionLLSRQ</eb:Service>
                    <eb:Action>EndTransactionLLSRQ</eb:Action>
                    <eb:MessageData>
                        <eb:MessageId>mid:20001209-133003-2333@clientofsabre.com</eb:MessageId>
                        <eb:Timestamp>{current_timestamp}Z</eb:Timestamp>
                    </eb:MessageData>
                    </eb:MessageHeader>
                    <eb:Security xmlns:eb="http://schemas.xmlsoap.org/ws/2002/12/secext" soapenv:mustUnderstand="0">
                    <eb:BinarySecurityToken>{token}</eb:BinarySecurityToken>
                    </eb:Security>
                </soapenv:Header>
                <soapenv:Body>
                    <EndTransactionRQ Version="2.0.8" xmlns="http://webservices.sabre.com/sabreXML/2011/10" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                        <EndTransaction Ind="true" />
                    </EndTransactionRQ>
                </soapenv:Body>
            </soapenv:Envelope>"""

    def ignoreTransactionRQ(self):
        pass

    def sabreCommandLLSRQ(self, pcc, token, conversation_id, command):


        return f"""<?xml version="1.0" encoding="UTF-8"?>
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
                <soapenv:Header>
                    <eb:MessageHeader xmlns:eb="http://www.ebxml.org/namespaces/messageHeader" soapenv:mustUnderstand="0">
                        <eb:From>
                            <eb:PartyId />
                        </eb:From>
                        <eb:To>
                            <eb:PartyId />
                        </eb:To>
                        <eb:CPAId>{pcc}</eb:CPAId>
                        <eb:ConversationId>{conversation_id}</eb:ConversationId>
                        <eb:Service>SabreCommandLLSRQ</eb:Service>
                        <eb:Action>SabreCommandLLSRQ</eb:Action>
                        <eb:MessageData>
                            <eb:MessageId>mid:20001209-133003-2333@clientofsabre.com</eb:MessageId>
                            <eb:Timestamp>{self.current_timestamp}</eb:Timestamp>
                        </eb:MessageData>
                    </eb:MessageHeader>
                    <eb:Security xmlns:eb="http://schemas.xmlsoap.org/ws/2002/12/secext" soapenv:mustUnderstand="0">
                        <eb:BinarySecurityToken>{token}</eb:BinarySecurityToken>
                    </eb:Security>
                </soapenv:Header>
                <soapenv:Body>
                    <SabreCommandLLSRQ xmlns="http://webservices.sabre.com/sabreXML/2003/07" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" Version="1.8.1">
                        <Request Output="SCREEN" CDATA="true">
                            <HostCommand>{command}</HostCommand>
                        </Request>
                    </SabreCommandLLSRQ>
                </soapenv:Body>
            </soapenv:Envelope>"""

    def getReservationRQ(self, pcc, token, conversation_id, record_locator):


        return f"""<?xml version="1.0" encoding="UTF-8"?>
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
                <soapenv:Header>
                    <eb:MessageHeader xmlns:eb="http://www.ebxml.org/namespaces/messageHeader" soapenv:mustUnderstand="0">
                        <eb:From>
                            <eb:PartyId />
                        </eb:From>
                        <eb:To>
                            <eb:PartyId />
                        </eb:To>
                        <eb:CPAId>{pcc}</eb:CPAId>
                        <eb:ConversationId>{conversation_id}</eb:ConversationId>
                        <eb:Service>getReservationRQ</eb:Service>
                        <eb:Action>getReservationRQ</eb:Action>
                        <eb:MessageData>
                            <eb:MessageId>mid:20001209-133003-2333@clientofsabre.com</eb:MessageId>
                            <eb:Timestamp>{self.current_timestamp}Z</eb:Timestamp>
                        </eb:MessageData>
                    </eb:MessageHeader>
                    <eb:Security xmlns:eb="http://schemas.xmlsoap.org/ws/2002/12/secext" soapenv:mustUnderstand="0">
                        <eb:BinarySecurityToken>{token}</eb:BinarySecurityToken>
                    </eb:Security>
                </soapenv:Header>
                <soapenv:Body>
                    <GetReservationRQ xmlns="http://webservices.sabre.com/pnrbuilder/v1_18" Version="1.18.0">
                    <Locator>{record_locator}</Locator>
                    <RequestType>Stateful</RequestType>
                    <ReturnOptions UnmaskCreditCard="true" ShowTicketStatus="false" Language="US">
                        <SubjectAreas>
                        <SubjectArea>AIR_CABIN</SubjectArea>
                        <SubjectArea>ITINERARY</SubjectArea>
                        <SubjectArea>PRICE_QUOTE</SubjectArea>
                        <SubjectArea>ANCILLARY</SubjectArea>
                        </SubjectAreas>

                        <ResponseFormat>STL</ResponseFormat>
                    </ReturnOptions>
                    </GetReservationRQ>
                </soapenv:Body>
            </soapenv:Envelope>"""
