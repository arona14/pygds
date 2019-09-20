from pygds.core.types import PassengerUpdate, FlightSeatMap
from pygds.core.security_utils import generate_random_message_id, generate_created
from pygds.sabre.xmlbuilders.update_passenger_sub_parts import passenger_info, customer_id, service_ssr_code, seat_request
from pygds.sabre.xmlbuilders.sub_parts import get_segment_number, get_passenger_type, get_commision, get_fare_type, get_segments_exchange, get_passengers_exchange, \
    get_form_of_payment, get_commission_exchange, add_flight_segments_to_air_book, store_commission, store_name_select, store_pax_type, store_plus_up, \
    store_ticket_designator, add_flight_segment


class SabreXMLBuilder:
    """This class can generate XML needed for sabre soap requests."""

    def __init__(self, url: str, username: str, password: str, pcc: str):
        self.current_timestamp = generate_created()
        self.url = url
        self.username = username
        self.password = password
        self.pcc = pcc
        self.conversation_id = generate_random_message_id()

    def generate_header(self, service_name, action_code, token):

        return f"""<soapenv:Header>
            <eb:MessageHeader xmlns:eb="http://www.ebxml.org/namespaces/messageHeader" soapenv:mustUnderstand="0">
                <eb:From>
                    <eb:PartyId />
                </eb:From>
                <eb:To>
                    <eb:PartyId />
                </eb:To>
                <eb:CPAId>{self.pcc}</eb:CPAId>
                <eb:ConversationId>{self.conversation_id}</eb:ConversationId>
                <eb:Service>{service_name}</eb:Service>
                <eb:Action>{action_code}</eb:Action>
                <eb:MessageData>
                    <eb:MessageId>mid:20001209-133003-2333@clientofsabre.com</eb:MessageId>
                    <eb:Timestamp>{self.current_timestamp}Z</eb:Timestamp>
                </eb:MessageData>
            </eb:MessageHeader>
            <eb:Security xmlns:eb="http://schemas.xmlsoap.org/ws/2002/12/secext" soapenv:mustUnderstand="0">
                <eb:BinarySecurityToken>{token}</eb:BinarySecurityToken>
            </eb:Security>
        </soapenv:Header>"""

    def session_create_rq(self, conversation_id: str):
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

    def session_token_rq(self):
        """ This will return a Token """
        conversation_id = generate_random_message_id()

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
                        <eb:ConversationId>{conversation_id}</eb:ConversationId>
                        <eb:Service>Session</eb:Service>
                        <eb:Action>TokenCreateRQ</eb:Action>
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
                    <TokenCreateRQ Version="1.0.0"/>
                 </soap-env:Body>
            </soap-env:Envelope>"""

    def end_transaction_rq(self, token):
        """ end transaction xml"""
        header = self.generate_header("EndTransactionLLSRQ", "EndTransactionLLSRQ", token)
        return f"""<?xml version="1.0" encoding="UTF-8"?>
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
                {header}
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
        header = self.generate_header("SabreCommandLLSRQ", "SabreCommandLLSRQ", token)
        return f"""<?xml version="1.0" encoding="UTF-8"?>
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
                {header}
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
        header = self.generate_header("GetReservationRQ", "GetReservationRQ", token)
        return f"""<?xml version="1.0" encoding="UTF-8"?>
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
                {header}
                <soapenv:Body>
                    <ns7:GetReservationRQ xmlns:ns7="http://webservices.sabre.com/pnrbuilder/v1_18" Version="1.18.0">
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

    def price_quote_rq(self, token, retain: bool, tour_code: str = '', fare_type: str = '', segment_select: list = [], passenger_type: list = [], baggage: int = 0, region_name: str = "", brand_id: str = None):
        """
            Return the xml request to price air itineraries
        """
        if retain:
            name_select = store_name_select(passenger_type)
            name_select = name_select if name_select else ""
            ticket_designator, segment_number = store_ticket_designator(passenger_type, segment_select, brand_id)
            pax_type = store_pax_type(passenger_type)
            pax_type = pax_type if pax_type else ""
            commission = store_commission(fare_type, passenger_type, region_name, self.pcc)
            # tour_code = store_tour_code(passenger_type)
            plus_up = store_plus_up(passenger_type, self.pcc)
            plus_up = plus_up if plus_up else ""
            fare_type_value = ""
        else:
            segment_number = get_segment_number(segment_select)
            pax_type, name_select = get_passenger_type(passenger_type, fare_type)
            fare_type_value = get_fare_type(fare_type) if get_fare_type(fare_type) else ""
            commission = get_commision(baggage, self.pcc, region_name)
            plus_up = ""
            ticket_designator = ""
        header = self.generate_header("Session", "OTA_AirPriceLLSRQ", token)
        return f"""<?xml version="1.0" encoding="UTF-8"?>
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
                {header}
                <soapenv:Body>
                    <OTA_AirPriceRQ Version="2.17.0" xmlns="http://webservices.sabre.com/sabreXML/2011/10" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                        <PriceRequestInformation Retain="{str(retain).lower()}">
                        <OptionalQualifiers>
                            {commission}
                            <PricingQualifiers>
                                {fare_type_value}
                                {ticket_designator}
                                {segment_number}
                                {name_select}
                                {pax_type}
                                {plus_up}
                            </PricingQualifiers>
                        </OptionalQualifiers>
                        </PriceRequestInformation>
                    </OTA_AirPriceRQ>
                </soapenv:Body>
            </soapenv:Envelope>"""

    def queue_place_rq(self, token, queue_number, record_locator):
        header = self.generate_header("QueuePlaceLLSRQ", "QueuePlaceLLSRQ", token)
        return f"""<?xml version="1.0" encoding="UTF-8"?>
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
                {header}
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
        header = self.generate_header("VoidTicketLLSRQ", "VoidTicketLLSRQ", token)
        return f"""<?xml version="1.0" encoding="UTF-8"?>
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
                {header}
                <soapenv:Body>
                    <VoidTicketRQ Version="2.1.0" xmlns="http://webservices.sabre.com/sabreXML/2011/10" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                        <Ticketing RPH="{rph}" />
                    </VoidTicketRQ>
                </soapenv:Body>
            </soapenv:Envelope>"""

    def cancel_segment_rq(self, token, segment):
        """
        Return the xml request to to cancel itinerary
        segments contained within a PNR

        """
        header = self.generate_header("OTA_CancelLLSRQ", "OTA_CancelLLSRQ", token)
        return f"""<?xml version="1.0" encoding="UTF-8"?>
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
               {header}
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
        flight_segment = add_flight_segments_to_air_book(flight_segment)
        header = self.generate_header("EnhancedAirBookRQ", "EnhancedAirBookRQ", token)
        return f"""<?xml version="1.0" encoding="UTF-8"?>
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
                {header}
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

    def update_passenger_rq(self, token, pnr, p_update: PassengerUpdate):
        """
            Return the xml request to update a passenger in pnr
        """
        header = self.generate_header("PassengerDetailsRQ", "PassengerDetailsRQ", token)
        if p_update.name_number:
            seat_part = seat_request(p_update.name_number, p_update.seat_number,
                                     p_update.segment_number) if p_update.seat_number and p_update.segment_number else ""
            passenger_info_part = passenger_info(p_update.date_of_birth, p_update.gender, p_update.name_number,
                                                 p_update.first_name, p_update.last_name) if p_update.date_of_birth and p_update.gender and p_update.first_name and p_update.last_name else ""
            service_ssr_part = service_ssr_code(p_update.segment_number, p_update.ssr_code, p_update.name_number) if p_update.segment_number and p_update.ssr_code else ""
        else:
            seat_part, passenger_info_part, service_ssr_part = ("", "", "")

        dk_number_part = customer_id(p_update.dk_number) if p_update.dk_number else ""

        return f"""<?xml version="1.0" encoding="UTF-8"?>
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
                {header}
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
                            {seat_part}
                            <SpecialServiceRQ>
                            <SpecialServiceInfo>
                                {passenger_info_part}
                                {service_ssr_part}
                            </SpecialServiceInfo>
                            </SpecialServiceRQ>
                        </SpecialReqDetails>
                            {dk_number_part}
                    </PassengerDetailsRQ>
                </soapenv:Body>
            </soapenv:Envelope>"""

    def info_credit_card(self, code_cc, expire_date, cc_number, commission_value, approval_code=None):
        return f"""<FOP_Qualifiers>
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

    def seap_map_rq(self, token, flight_infos: FlightSeatMap):
        """
            Return the xml request to search a seap map
        """
        header = self.generate_header("EnhancedSeatMapRQ", "EnhancedSeatMapRQ", token)
        flight_info = add_flight_segment(flight_infos.origin, flight_infos.destination, flight_infos.depart_date, flight_infos.operating_code, flight_infos.marketing_code, flight_infos.flight_number, flight_infos.arrival_date, flight_infos.class_of_service, flight_infos.currency_code)
        return f"""<?xml version="1.0" encoding="UTF-8"?>
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
               {header}
                <soapenv:Body>
                    <tag0:EnhancedSeatMapRQ xmlns:tag0="http://stl.sabre.com/Merchandising/v6" version="6">
                        <tag0:RequestType>Payload</tag0:RequestType>
                        <tag0:SeatMapQueryEnhanced correlationID="20190218103518">
                                {flight_info}
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
        header = self.generate_header("TKT_ElectronicDocumentServicesRQ", "TKT_ElectronicDocumentServicesRQ", token)
        return f"""<?xml version="1.0" encoding="UTF-8"?>
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
                {header}
                <soapenv:Body>
                    <GetElectronicDocumentRQ Version="1.0.0" requestType="H" xmlns="http://www.sabre.com/ns/Ticketing/EDoc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sabre.com/ns/Ticketing/EDoc TKT_ElectronicDocumentServices_v.1.0.0.xsd">
                            <ns1:STL_Header.RQ xmlns:ns1="http://www.sabre.com/ns/Ticketing/EDocStl"/>
                            <ns2:POS xmlns:ns2="http://www.sabre.com/ns/Ticketing/EDocStl"/>
                            <SearchParameters>
                                <DocumentNumber>{str(ticket_number)}</DocumentNumber>
                            </SearchParameters>
                    </GetElectronicDocumentRQ>
                </soapenv:Body>
            </soapenv:Envelope>"""

    def exchange_shopping_rq(self, token, pnr, passengers_info, origin_destination_info):
        """
            Return the xml request to search for available flights
            for a ticket number to be exchanged
        """
        header = self.generate_header("ExchangeShoppingRQ", "ExchangeShoppingRQ", token)
        return f"""<?xml version="1.0" encoding="UTF-8"?>
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
               {header}
                <soapenv:Body>
                    <ExchangeShoppingRQ xmlns="http://services.sabre.com/sp/exchange/shopping/v2_3" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="2.3.0">
                        <STL_Header.RQ>
                            <OrchestrationID seq="0">231488734192050161</OrchestrationID>
                        </STL_Header.RQ>
                        <TicketingProvider>1S</TicketingProvider>
                        <PassengerInformation>
                            {get_passengers_exchange(pnr, passengers_info)}
                        </PassengerInformation>
                            {get_segments_exchange(origin_destination_info)}
                    </ExchangeShoppingRQ>
                </soapenv:Body>
            </soapenv:Envelope>"""

    def automated_exchanges_price_rq(self, token, ticket_number, name_number, passenger_type):
        """
            Return the xml request to find new prices
            for a ticket number to be exchanged
        """
        header = self.generate_header("AutomatedExchangesLLSRQ", "AutomatedExchangesLLSRQ", token)
        return f"""<?xml version="1.0" encoding="UTF-8"?>
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
                {header}
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

    def automated_exchanges_commmit_rq(self, token, price_quote, form_of_payment, fare_type, percent, amount):
        """
            Return the xml request to store a price
            for a ticket number to be exchanged
        """
        header = self.generate_header("AutomatedExchangesLLSRQ", "AutomatedExchangesLLSRQ", token)

        if percent is not None and percent > 0:
            commission = get_commission_exchange(fare_type, percent)

        elif amount is not None and amount > 0:
            commission = get_commission_exchange(fare_type, amount)
        else:
            commission = ""

        return f"""<?xml version="1.0" encoding="UTF-8"?>
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
                {header}
                <soapenv:Body>
                    <AutomatedExchangesRQ xmlns="http://webservices.sabre.com/sabreXML/2011/10" ReturnHostCommand="true" Version="2.7.0">
                        <ExchangeConfirmation PQR_Number="{price_quote}">
                            <OptionalQualifiers>
                                <FOP_Qualifiers>
                                    {get_form_of_payment(payment_type = form_of_payment["payment_type"], code_card = form_of_payment["code_card"], expire_date = form_of_payment["expire_date"], cc_number = form_of_payment["cc_number"])}
                                </FOP_Qualifiers>
                                {commission}
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
        header = self.generate_header("IgnoreTransactionLLSRQ", "IgnoreTransactionLLSRQ", token)
        return f"""<?xml version="1.0" encoding="UTF-8"?>
                <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
                    {header}
                    <soapenv:Body>
                        <IgnoreTransactionRQ xmlns="http://webservices.sabre.com/sabreXML/2011/10" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" Version="2.0.0"/>
                    </soapenv:Body>
                </soapenv:Envelope>"""

    def credit_verification_rq(self, token, airline_code, code_cc, expire_date, cc_number, total_fare, currency_code):
        """
            Return the xml request to check the information of a bank account number
        """
        header = self.generate_header("CreditVerificationLLSRQ", "CreditVerificationLLSRQ", token)

        return f"""<?xml version="1.0" encoding="UTF-8"?>
                <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
                    {header}
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
        header = self.generate_header("PassengerDetailsRQ", "PassengerDetailsRQ", token)

        return f"""<?xml version="1.0" encoding="UTF-8"?>
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
                {header}
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

    def fop_choice(self, code_cc=None, expire_date=None, cc_number=None, approval_code=None, payment_type=None, commission_value=None):
        fop = ""
        if code_cc and expire_date and cc_number is not None:
            fop = self.info_credit_card(code_cc, expire_date, cc_number, approval_code, commission_value)
        elif payment_type and commission_value is not None:
            fop = self.info_cash_or_cheque(payment_type, commission_value)
        return fop

    def get_name_select(self, name_select=None):

        return f"""<NameSelect NameNumber="{name_select}"/>""" if name_select else ""

    def air_ticket_rq(self, token_value, price_quote, code_cc, expire_date, cc_number, approval_code, payment_type, commission_value, name_select):
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
                                {self.fop_choice(code_cc, expire_date, cc_number, approval_code, payment_type, commission_value)}
                                <PricingQualifiers>
                                    <PriceQuote>
                                        {self.get_name_select(name_select)}
                                        <Record Number="{price_quote}"/>
                                    </PriceQuote>
                                </PricingQualifiers>
                            </OptionalQualifiers>
                        </AirTicketRQ>
                    </soapenv:Body>
            </soapenv:Envelope>"""
