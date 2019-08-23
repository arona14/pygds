from pygds.core.security_utils import generate_random_message_id, generate_created

class SabreXMLBuilder:
    """This class can generate XML needed for sabre soap requests."""

    def __init__(self, url: str, username: str, password: str, pcc: str):
        self.current_timestamp = generate_created()
        self.url = url
        self.username = username
        self.password = password
        self.pcc = pcc
        self.conversation_id = generate_random_message_id()

    def generate_header(self, pcc, conversation_id, token_value):
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
                            <eb:CPAId>{self.pcc}</eb:CPAId>
                            <eb:ConversationId>{self.conversation_id}</eb:ConversationId>
                            <eb:Service>AirTicketLLSRQ</eb:Service>
                            <eb:Action>AirTicketLLSRQ</eb:Action>
                            <eb:MessageData>
                                <eb:MessageId>mid:20001209-133003-2333@clientofsabre.com</eb:MessageId>
                                <eb:Timestamp>{self.current_timestamp}</eb:Timestamp>
                            </eb:MessageData>
                            <Description>CTS-PORTAL</Description>
                        </eb:MessageHeader>
                        <eb:Security xmlns:eb="http://schemas.xmlsoap.org/ws/2002/12/secext" soapenv:mustUnderstand="0">
                        <eb:BinarySecurityToken>{token_value}</eb:BinarySecurityToken>
                        <eb:group>{self.pcc}</eb:group>
                        </eb:Security>
                    </soapenv:Header>"""

    def session_create_rq(self, pcc, user_name, password, conversation_id):
        """Return the xml request to create a session."""

    def session_create_rq(self):
        """
            Return the xml request to initiate a SOAP API session
        """
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
                        <eb:CPAId>{self.pcc}</eb:CPAId>
                        <eb:ConversationId>{self.conversation_id}</eb:ConversationId>
                        <eb:Service>SessionCreateRQ</eb:Service>
                        <eb:Action>SessionCreateRQ</eb:Action>
                        <eb:MessageData>
                            <eb:MessageId>mid:20001209-133003-2333@clientofsabre.com</eb:MessageId>
                            <eb:Timestamp>{self.current_timestamp}Z</eb:Timestamp>
                        </eb:MessageData>
                    </eb:MessageHeader>
                    <wsse:Security xmlns:wsse="http://schemas.xmlsoap.org/ws/2002/12/secext" xmlns:wsu="http://schemas.xmlsoap.org/ws/2002/12/utility">
                        <wsse:UsernameToken>
                            <wsse:Username>{self.username}</wsse:Username>
                            <wsse:Password>{self.password}</wsse:Password>
                            <Organization>{self.pcc}</Organization>
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
                            <Source PseudoCityCode="{self.pcc}"/>
                        </POS>
                    </SessionCreateRQ>
                    <ns:SessionCreateRQ xmlns:ns="http://www.opentravel.org/OTA/2002/11" />
                </soap-env:Body>
            </soap-env:Envelope>"""

    def session_close_rq(self, token):
        """
            Return the xml request to close a SOAP API session
        """
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
                            <ns3:CPAId>{self.pcc}</ns3:CPAId>
                        <ns3:ConversationId>{self.conversation_id}</ns3:ConversationId>
                            <ns3:Service>SessionCloseRQ</ns3:Service>
                            <ns3:Action>SessionCloseRQ</ns3:Action>
                            </ns3:MessageHeader>
                        <ns5:Security xmlns:ns2="http://www.w3.org/2000/09/xmldsig#"
                            xmlns:ns3="http://www.ebxml.org/namespaces/messageHeader"
                            xmlns:ns4="http://www.w3.org/1999/xlink"
                                xmlns:ns5="http://schemas.xmlsoap.org/ws/2002/12/secext">
                        <ns5:BinarySecurityToken>{token}</ns5:BinarySecurityToken>
                        <ns2:group>{self.pcc}</ns2:group>
                        </ns5:Security>
                </SOAP-ENV:Header>
                <SOAP-ENV:Body>
                    <SessionCloseRQ status="Approved" version="1" xmlns="http://www.opentravel.org/OTA/2002/11"/>
                </SOAP-ENV:Body>
            </SOAP-ENV:Envelope>"""

    def end_transaction_rq(self, token):
        """
            Return the xml request to complete and store 
            changes made to a Passenger Name Record (PNR)
        """
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
                    <eb:CPAId>{self.pcc}</eb:CPAId>
                    <eb:ConversationId>{self.conversation_id}</eb:ConversationId>
                    <eb:Service>EndTransactionLLSRQ</eb:Service>
                    <eb:Action>EndTransactionLLSRQ</eb:Action>
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
                    <EndTransactionRQ Version="2.0.8" xmlns="http://webservices.sabre.com/sabreXML/2011/10" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                        <EndTransaction Ind="true" />
                    </EndTransactionRQ>
                </soapenv:Body>
            </soapenv:Envelope>"""

    def sabre_command_lls_rq(self, token, command):
        """
            Return the xml request to send a command
        """
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
                        <eb:CPAId>{self.pcc}</eb:CPAId>
                        <eb:ConversationId>{self.conversation_id}</eb:ConversationId>
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

    def get_reservation_rq(self, token, record_locator):
        """
            Return the xml request to retrieve and 
            display a passenger name record (PNR)
        """
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
                        <eb:CPAId>{self.pcc}</eb:CPAId>
                        <eb:ConversationId>{self.conversation_id}</eb:ConversationId>
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
                    <ns7:GetReservationRQ xmlns:ns7="http://webservices.sabre.com/pnrbuilder/v1_19" Version="1.19.0">
                        <ns7:Locator>{record_locator}</ns7:Locator>
                        <ns7:RequestType>Stateful</ns7:RequestType>
                        <ns7:ReturnOptions>
                            <ns7:SubjectAreas>
                                <ns7:SubjectArea>AIR_CABIN</ns7:SubjectArea>
                                <ns7:SubjectArea>ITINERARY</ns7:SubjectArea>
                                <ns7:SubjectArea>PRICE_QUOTE</ns7:SubjectArea>
                                <ns7:SubjectArea>ANCILLARY</ns7:SubjectArea>
                            </ns7:SubjectAreas>
                            <ns7:ResponseFormat>STL</ns7:ResponseFormat>
                        </ns7:ReturnOptions>
                    </ns7:GetReservationRQ>
                </soapenv:Body>
            </soapenv:Envelope>"""
    
    def price_quote_rq(self, token, retain, commission, tour_code, fare_type, ticket_designator, segment_select, name_select, passenger_type, plus_up):
        """
            Return the xml request to price air itineraries
        """
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
                    <eb:CPAId>{self.pcc}</eb:CPAId>
                    <eb:ConversationId>{self.conversation_id}</eb:ConversationId>
                    <eb:Service>Session</eb:Service>
                    <eb:Action>OTA_AirPriceLLSRQ</eb:Action>
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
                    <OTA_AirPriceRQ Version="2.17.0" xmlns="http://webservices.sabre.com/sabreXML/2011/10" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                        <PriceRequestInformation Retain="{retain}">
                        <OptionalQualifiers>
                            {commission}
                            {tour_code}
                            <PricingQualifiers>
                                {fare_type}
                                {ticket_designator}
                                {segment_select}
                                {name_select}
                                {passenger_type}
                                {plus_up}
                            </PricingQualifiers>
                        </OptionalQualifiers>
                        </PriceRequestInformation>
                    </OTA_AirPriceRQ>
                </soapenv:Body>
            </soapenv:Envelope>"""
    
    def queue_place_rq(self, token, queue_number, record_locator):
        """
            Return the xml request to place a pnr in a queue
        """
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
                        <eb:CPAId>{self.pcc}</eb:CPAId>
                        <eb:ConversationId>{self.conversation_id}</eb:ConversationId>
                        <eb:Service>QueuePlaceLLSRQ</eb:Service>
                        <eb:Action>QueuePlaceLLSRQ</eb:Action>
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
                    <QueuePlaceRQ xmlns="http://webservices.sabre.com/sabreXML/2011/10" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ReturnHostCommand="false" TimeStamp="2014-09-07T09:30:00-06:00" Version="2.0.4">
                        <QueueInfo>
                            <QueueIdentifier  Number="{queue_number}" PrefatoryInstructionCode="11" PseudoCityCode="{self.pcc}"/>
                            <UniqueID ID="{record_locator}"/>
                        </QueueInfo>
                    </QueuePlaceRQ>
                </soapenv:Body>
            </soapenv:Envelope>"""
    
    def void_ticket_rq(self, token, rph):
        """
            Return the xml request to void air tickets
        """
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
                    <eb:CPAId>{self.pcc}</eb:CPAId>
                    <eb:ConversationId>{self.conversation_id}</eb:ConversationId>
                    <eb:Service>VoidTicketLLSRQ</eb:Service>
                    <eb:Action>VoidTicketLLSRQ</eb:Action>
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
                    <VoidTicketRQ Version="2.1.0" xmlns="http://webservices.sabre.com/sabreXML/2011/10" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                        <Ticketing RPH="{rph}" />
                    </VoidTicketRQ>
                </soapenv:Body>
            </soapenv:Envelope>"""
    
    def cancel_segment_rq(self, token, segment) :
        """
            Return the xml request to to cancel itinerary 
            segments contained within a PNR
        """    
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
                        <eb:CPAId>{self.pcc}</eb:CPAId>
                        <eb:ConversationId>{self.conversation_id}</eb:ConversationId>
                        <eb:Service>OTA_CancelLLSRQ</eb:Service>
                        <eb:Action>OTA_CancelLLSRQ</eb:Action>
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
                    <OTA_CancelRQ xmlns="http://webservices.sabre.com/sabreXML/2011/10" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" NumResponses="1" ReturnHostCommand="false" TimeStamp="2016-05-17T10:00:00-06:00" Version="2.0.2">
                        {segment}
                    </OTA_CancelRQ>
                </soapenv:Body>
            </soapenv:Envelope>"""

    def re_book_air_segment_rq(self, token, flight_segment, pnr):
        """
            Return the xml request to book flight  segment
        """
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
                        <eb:CPAId>{self.pcc}</eb:CPAId>
                        <eb:ConversationId>{self.conversation_id}</eb:ConversationId>
                        <eb:Service>EnhancedAirBookRQ</eb:Service>
                        <eb:Action>EnhancedAirBookRQ</eb:Action>
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
                    <EnhancedAirBookRQ version="3.9.0" xmlns="http://services.sabre.com/sp/eab/v3_9" HaltOnError="true">
                        <OTA_AirBookRQ>
                            <OriginDestinationInformation>
                                {flight_segment}
                            </OriginDestinationInformation>
                        </OTA_AirBookRQ>
                        <PostProcessing IgnoreAfter="false">
                            <RedisplayReservation/>
                        </PostProcessing>
                        <PreProcessing IgnoreBefore="false">
                            <UniqueID ID="{pnr}"/>
                        </PreProcessing>
                    </EnhancedAirBookRQ>
                </soapenv:Body>
            </soapenv:Envelope>"""
    
    def update_passenger_rq(self, token, pnr, air_seat, passenger, ssr_code, dk):
        """
            Return the xml request to update a passenger in pnr
        """
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
                        <eb:CPAId>{self.pcc}</eb:CPAId>
                        <eb:ConversationId>{self.conversation_id}</eb:ConversationId>
                        <eb:Service>PassengerDetailsRQ</eb:Service>
                        <eb:Action>PassengerDetailsRQ</eb:Action>
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
                    <PassengerDetailsRQ xmlns="http://services.sabre.com/sp/pd/v3_4" version="3.4.0">
                            <PostProcessing unmaskCreditCard="false">
                                <EndTransactionRQ>
                                    <EndTransaction Ind="false"></EndTransaction>
                                    <Source ReceivedFrom="WEBSERVICES"></Source>
                                </EndTransactionRQ>
                            </PostProcessing>
                            <PreProcessing ignoreBefore="false">
                                <UniqueID id="{pnr}"/>
                            </PreProcessing>
                        <SpecialReqDetails>
                            {air_seat}
                            <SpecialServiceRQ>
                            <SpecialServiceInfo>
                                {passenger}
                                {ssr_code}
                            </SpecialServiceInfo>
                            </SpecialServiceRQ>
                        </SpecialReqDetails>
                            {dk}
                    </PassengerDetailsRQ>
                </soapenv:Body>
            </soapenv:Envelope>"""


    def info_credit_card(self, code_cc, expire_date, cc_number, commission_value, approval_code=None):
        return  f"""<FOP_Qualifiers>
                <BasicFOP>
                    <CC_Info Suppress="true">
                        <PaymentCard Code="{code_cc}" ExpireDate="{expire_date}" ManualApprovalCode ="{approval_code}" Number="{cc_number}"/>
                    </CC_Info>
                </BasicFOP>
                </FOP_Qualifiers>
                {commission_value}"""


    def info_cash_or_cheque(self, payment_type, commission_value):
        payment_infos = f"""<FOP_Qualifiers>
                <BasicFOP Type="{payment_type}"/>
                </FOP_Qualifiers>
                {commission_value}"""
        return payment_infos
   
    def seap_map_rq(self, token, flight_infos):
        """
            Return the xml request to search a seap map
        """
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
                        <eb:CPAId>{self.pcc}</eb:CPAId>
                        <eb:ConversationId>{self.conversation_id}</eb:ConversationId>
                        <eb:Service>EnhancedSeatMapRQ</eb:Service>
                        <eb:Action>EnhancedSeatMapRQ</eb:Action>
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
                    <tag0:EnhancedSeatMapRQ xmlns:tag0="http://stl.sabre.com/Merchandising/v6" version="6">
                        <tag0:RequestType>Payload</tag0:RequestType>
                        <tag0:SeatMapQueryEnhanced correlationID="20190218103518">
                                {flight_infos}
                            <tag0:POS>
                            <tag0:PCC>{self.pcc}</tag0:PCC>
                            </tag0:POS>
                        </tag0:SeatMapQueryEnhanced>
                    </tag0:EnhancedSeatMapRQ>
                </soapenv:Body>
            </soapenv:Envelope>"""
    
    def electronic_document_rq(self, token, ticket_number):
        """
            Return the xml request to check if a ticket number is exchangeable
        """
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
                        <eb:CPAId>{self.pcc}</eb:CPAId>
                        <eb:ConversationId>{self.conversation_id}</eb:ConversationId>
                        <eb:Service>TKT_ElectronicDocumentServicesRQ</eb:Service>
                        <eb:Action>TKT_ElectronicDocumentServicesRQ</eb:Action>
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
                    <GetElectronicDocumentRQ Version="1.0.0" requestType="H" xmlns="http://www.sabre.com/ns/Ticketing/EDoc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sabre.com/ns/Ticketing/EDoc TKT_ElectronicDocumentServices_v.1.0.0.xsd">
                            <ns1:STL_Header.RQ xmlns:ns1="http://www.sabre.com/ns/Ticketing/EDocStl"/>
                            <ns2:POS xmlns:ns2="http://www.sabre.com/ns/Ticketing/EDocStl"/>
                            <SearchParameters>
                                {ticket_number}
                            </SearchParameters>
                    </GetElectronicDocumentRQ>
                </soapenv:Body>
            </soapenv:Envelope>"""
    
    def exchange_shopping_rq(self, token, passengers_info, origin_destination_info):
        """
            Return the xml request to search for available flights 
            for a ticket number to be exchanged
        """
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
                        <eb:CPAId>{self.pcc}</eb:CPAId>
                        <eb:ConversationId>{self.conversation_id}</eb:ConversationId>
                        <eb:Service>ExchangeShoppingRQ</eb:Service>
                        <eb:Action>ExchangeShoppingRQ</eb:Action>
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
                    <ExchangeShoppingRQ xmlns="http://services.sabre.com/sp/exchange/shopping/v2_3" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="2.3.0">
                        <STL_Header.RQ>
                            <OrchestrationID seq="0">231488734192050161</OrchestrationID>
                        </STL_Header.RQ>
                        <TicketingProvider>1S</TicketingProvider>
                        <PassengerInformation>
                            {passengers_info}
                        </PassengerInformation>
                            {origin_destination_info}
                    </ExchangeShoppingRQ>
                </soapenv:Body>
            </soapenv:Envelope>"""
        
    def automated_exchanges_price_rq(self, token, ticket_number, name_number, passenger_type):
        """
            Return the xml request to find new prices 
            for a ticket number to be exchanged
        """
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
                        <eb:CPAId>{self.pcc}</eb:CPAId>
                        <eb:ConversationId>{self.conversation_id}</eb:ConversationId>
                        <eb:Service>AutomatedExchangesLLSRQ</eb:Service>
                        <eb:Action>AutomatedExchangesLLSRQ</eb:Action>
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
                    <AutomatedExchangesRQ xmlns="http://webservices.sabre.com/sabreXML/2011/10" ReturnHostCommand="true" Version="2.7.0">
                        <ExchangeComparison OriginalTicketNumber="{ticket_number}">
                            <PriceRequestInformation>
                                <OptionalQualifiers>
                                    <PricingQualifiers>
                                        <NameSelect NameNumber="{name_number}"/>
                                        <PassengerType Code="{passenger_type}"/>
                                    </PricingQualifiers>
                                </OptionalQualifiers>
                            </PriceRequestInformation>
                        </ExchangeComparison>
                    </AutomatedExchangesRQ>
                </soapenv:Body>
            </soapenv:Envelope>"""
           
    def automated_exchanges_commmit_rq(self, token, price_quote, form_of_payment, commission_value):
        """
            Return the xml request to store a price 
            for a ticket number to be exchanged
        """    
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
                        <eb:CPAId>{self.pcc}</eb:CPAId>
                        <eb:ConversationId>{self.conversation_id}</eb:ConversationId>
                        <eb:Service>AutomatedExchangesLLSRQ</eb:Service>
                        <eb:Action>AutomatedExchangesLLSRQ</eb:Action>
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
                    <AutomatedExchangesRQ xmlns="http://webservices.sabre.com/sabreXML/2011/10" ReturnHostCommand="true" Version="2.7.0">
                        <ExchangeConfirmation PQR_Number="{price_quote}">
                            <OptionalQualifiers>
                                <FOP_Qualifiers>
                                    {form_of_payment}
                                </FOP_Qualifiers>
                                {commission_value}
                            </OptionalQualifiers>
                        </ExchangeConfirmation>
                    </AutomatedExchangesRQ>
                </soapenv:Body>
            </soapenv:Envelope>"""
       
    def ticketing_exchange_rq(self, token, price_quote):
        """
            Return the xml request to ticket a pnr to be exchanged
        """
        return f"""<?xml version="1.0" encoding="UTF-8"?>
                <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
                    <soapenv:Header>
                        <eb:MessageHeader xmlns:eb="http://www.ebxml.org/namespaces/messageHeader" soapenv:mustUnderstand="0">
                            <eb:From>
                                <eb:PartyId>sample.url.of.sabre.client.com</eb:PartyId>
                            </eb:From>
                            <eb:To>
                                <eb:PartyId>webservices.sabre.com</eb:PartyId>
                            </eb:To>
                            <eb:CPAId>{self.pcc}</eb:CPAId>
                            <eb:ConversationId>{self.conversation_id}</eb:ConversationId>
                            <eb:Service>AirTicketLLSRQ</eb:Service>
                            <eb:Action>AirTicketLLSRQ</eb:Action>
                            <eb:MessageData>
                                <eb:MessageId>mid:20001209-133003-2333@clientofsabre.com</eb:MessageId>
                                <eb:Timestamp>{self.current_timestamp}</eb:Timestamp>
                            </eb:MessageData>
                            <Description>CTS-PORTAL</Description>
                        </eb:MessageHeader>
                        <eb:Security xmlns:eb="http://schemas.xmlsoap.org/ws/2002/12/secext" soapenv:mustUnderstand="0">
                        <eb:BinarySecurityToken>{token}</eb:BinarySecurityToken>
                        <eb:group>{self.pcc}</eb:group>
                        </eb:Security>
                    </soapenv:Header>
                    <soapenv:Body>
                        <AirTicketRQ Version="2.12.0" xmlns="http://webservices.sabre.com/sabreXML/2011/10" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" NumResponses="1" ReturnHostCommand="true">
                            <OptionalQualifiers>
                                <PricingQualifiers>
                                    <PriceQuote>
                                        <Record Number="{price_quote}" Reissue="true"/>
                                    </PriceQuote>
                                </PricingQualifiers>
                            </OptionalQualifiers>
                        </AirTicketRQ>
                    </soapenv:Body>
                </soapenv:Envelope>"""
        
    def ignore_transaction_rq(self, token):
        """Return the xml request to ignore a transaction."""
      
        return f"""<?xml version="1.0" encoding="UTF-8"?>
                <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
                    <soapenv:Header>
                        <eb:MessageHeader xmlns:eb="http://www.ebxml.org/namespaces/messageHeader" soapenv:mustUnderstand="0">
                            <eb:From>
                                <eb:PartyId>sample.url.of.sabre.client.com</eb:PartyId>
                            </eb:From>
                            <eb:To>
                                <eb:PartyId>webservices.sabre.com</eb:PartyId>
                            </eb:To>
                            <eb:CPAId>{self.pcc}</eb:CPAId>
                            <eb:ConversationId>{self.conversation_id}</eb:ConversationId>
                            <eb:Service>IgnoreTransactionLLSRQ</eb:Service>
                            <eb:Action>IgnoreTransactionLLSRQ</eb:Action>
                            <eb:MessageData>
                                <eb:MessageId>mid:20001209-133003-2333@clientofsabre.com</eb:MessageId>
                                <eb:Timestamp>{self.current_timestamp}</eb:Timestamp>
                            </eb:MessageData>
                            <Description>CTS-PORTAL</Description>
                        </eb:MessageHeader>
                        <eb:Security xmlns:eb="http://schemas.xmlsoap.org/ws/2002/12/secext" soapenv:mustUnderstand="0">
                            <eb:BinarySecurityToken>{token}</eb:BinarySecurityToken>
                        </eb:Security>
                    </soapenv:Header>
                    <soapenv:Body>
                        <IgnoreTransactionRQ xmlns="http://webservices.sabre.com/sabreXML/2011/10" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" Version="2.0.0"/>
                    </soapenv:Body>
                </soapenv:Envelope>"""
        
    def credit_verification_rq(self, token, airline_code, code_cc, expire_date, cc_number, total_fare, currency_code):
        """
            Return the xml request to check the information of a bank account number
        """
        return f"""<?xml version="1.0" encoding="UTF-8"?>
                <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
                    <soapenv:Header>
                        <eb:MessageHeader xmlns:eb="http://www.ebxml.org/namespaces/messageHeader" soapenv:mustUnderstand="0">
                            <eb:From>
                                <eb:PartyId>sample.url.of.sabre.client.com</eb:PartyId>
                            </eb:From>
                            <eb:To>
                                <eb:PartyId>webservices.sabre.com</eb:PartyId>
                            </eb:To>
                            <eb:CPAId>{self.pcc}</eb:CPAId>
                            <eb:ConversationId>{self.conversation_id}</eb:ConversationId>
                            <eb:Service>CreditVerificationLLSRQ</eb:Service>
                            <eb:Action>CreditVerificationLLSRQ</eb:Action>
                            <eb:MessageData>
                                <eb:MessageId>mid:20001209-133003-2333@clientofsabre.com</eb:MessageId>
                                <eb:Timestamp>{self.current_timestamp}</eb:Timestamp>
                            </eb:MessageData>
                            <Description>CTS-PORTAL</Description>
                        </eb:MessageHeader>
                        <eb:Security xmlns:eb="http://schemas.xmlsoap.org/ws/2002/12/secext" soapenv:mustUnderstand="0">
                            <eb:BinarySecurityToken>{token}</eb:BinarySecurityToken>
                        </eb:Security>
                    </soapenv:Header>
                    <soapenv:Body>
                        <CreditVerificationRQ xmlns="http://webservices.sabre.com/sabreXML/2011/10" ReturnHostCommand="true" Version="2.2.0">
                            <Credit>
                                <CC_Info>
                                    <PaymentCard AirlineCode="{airline_code}" Code="{code_cc}" ExpireDate="{expire_date}" Number="{cc_number}"/>
                                </CC_Info>
                                <ItinTotalFare>
                                    <TotalFare Amount="186.60" CurrencyCode="{currency_code}"/>
                                </ItinTotalFare>
                            </Credit>
                        </CreditVerificationRQ>
                    </soapenv:Body>
                </soapenv:Envelope>"""
        
    def send_remark_rq(self, token, text):
        """
            Return the xml request to add a remark for a pnr
        """
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
                        <eb:CPAId>{self.pcc}</eb:CPAId>
                        <eb:ConversationId>{self.conversation_id}</eb:ConversationId>
                        <eb:Service>PassengerDetailsRQ</eb:Service>
                        <eb:Action>PassengerDetailsRQ</eb:Action>
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
                    <PassengerDetailsRQ haltOnError="true" ignoreOnError="true" xmlns="http://services.sabre.com/sp/pd/v3_4" version="3.4.0">
                        <SpecialReqDetails>
                            <AddRemarkRQ>
                                <RemarkInfo>
                                    <Remark Type="General">
                                        <Text>{text}</Text>
                                    </Remark>
                                </RemarkInfo>
                            </AddRemarkRQ>
                        </SpecialReqDetails>
                    </PassengerDetailsRQ>
                </soapenv:Body>
            </soapenv:Envelope>"""
       
    def air_ticket_rq(self, token_value, info_ticketing, price_quote):
        """
            Return the xml request to issue air tickets
        """                        
        return f"""<?xml version="1.0" encoding="UTF-8"?>
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
                <soapenv:Header>
                    <eb:MessageHeader xmlns:eb="http://www.ebxml.org/namespaces/messageHeader" soapenv:mustUnderstand="0">
                        <eb:From>
                            <eb:PartyId>sample.url.of.sabre.client.com</eb:PartyId>
                        </eb:From>
                        <eb:To>
                            <eb:PartyId>webservices.sabre.com</eb:PartyId>
                        </eb:To>
                        <eb:CPAId>{self.pcc}</eb:CPAId>
                        <eb:ConversationId>{self.conversation_id}</eb:ConversationId>
                        <eb:Service>AirTicketLLSRQ</eb:Service>
                        <eb:Action>AirTicketLLSRQ</eb:Action>
                        <eb:MessageData>
                            <eb:MessageId>mid:20001209-133003-2333@clientofsabre.com</eb:MessageId>
                            <eb:Timestamp>{self.current_timestamp}</eb:Timestamp>
                        </eb:MessageData>
                        <Description>CTS-PORTAL</Description>
                    </eb:MessageHeader>
                    <eb:Security xmlns:eb="http://schemas.xmlsoap.org/ws/2002/12/secext" soapenv:mustUnderstand="0">
                    <eb:BinarySecurityToken>{token_value}</eb:BinarySecurityToken>
                    <eb:group>{self.pcc}</eb:group>
                    </eb:Security>
                </soapenv:Header>
                    <soapenv:Body>
                        <AirTicketRQ Version="2.12.0" xmlns="http://webservices.sabre.com/sabreXML/2011/10" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" NumResponses="1" ReturnHostCommand="true">
                            <OptionalQualifiers>
                                {info_ticketing}
                                <PricingQualifiers>
                                    <PriceQuote>
                                        <Record Number="{price_quote}"/>
                                    </PriceQuote>
                                </PricingQualifiers>
                            </OptionalQualifiers>
                        </AirTicketRQ>
                    </soapenv:Body>
            </soapenv:Envelope>"""
def main():
    pass