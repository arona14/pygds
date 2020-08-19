from typing import List

from pygds.core.helpers import get_data_from_json_safe as from_json_safe
from pygds.core.payment import FormOfPayment, CreditCard
from pygds.core.types import PassengerUpdate, FlightSeatMap, Passenger
from pygds.core.security_utils import generate_random_message_id, generate_created
from pygds.sabre.price import StoreSegmentSelect
from pygds.sabre.xmlbuilders.update_passenger_sub_parts import passenger_info, service_ssr_code, seat_request, travel_itinerary_add_info_rq
from pygds.sabre.xmlbuilders.sub_parts import get_segment_number, get_passenger_type, get_commision, get_fare_type, \
    get_segments_in_exchange_shopping, get_passengers_in_exchange_shopping, add_flight_segments_to_air_book, \
    store_commission, store_name_select, store_pax_type, store_plus_up, store_ticket_designator, add_flight_segment, \
    _store_single_name_select, _store_build_segment_selects, _store_single_pax_type, segments_to_cancel, \
    add_passenger_info, get_penalty_info, get_markup_exchange_price
from decimal import Decimal


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

    def session_create_rq(self, conversation_id: str, target_pcc: str = None):
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
                        <eb:CPAId>{target_pcc or self.pcc}</eb:CPAId>
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
                        <ns7:ReturnOptions UnmaskCreditCard="true">
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
                                {get_penalty_info()}
                            </PricingQualifiers>
                        </OptionalQualifiers>
                        </PriceRequestInformation>
                    </OTA_AirPriceRQ>
                </soapenv:Body>
            </soapenv:Envelope>"""

    def store_price_rq(self, token, fare_type: str, segment_select: List[StoreSegmentSelect], passenger_type: dict,
                       region_name: str = ""):
        """
            Return the xml request to price air itineraries
        """
        # TODO for now baggage is not used. Will add this tags in the future
        #             <BaggageAllowance Number="02" Weight="20">
        #                 <Segment EndNumber="3" Number="1"/>
        #             </BaggageAllowance>

        pax_type_code = passenger_type["code"]
        name_select = passenger_type["name_select"]
        ticket_designator = from_json_safe(passenger_type, "ticket_designator")

        name_select = _store_single_name_select(name_select)
        name_select = name_select if name_select else ""
        segment_numbers, brands, t_designator = _store_build_segment_selects(segment_select, ticket_designator, fare_type)
        pax_type = _store_single_pax_type(pax_type_code)
        pax_type = pax_type if pax_type else ""
        commission = store_commission(fare_type, passenger_type, region_name, self.pcc)
        # tour_code = store_tour_code(passenger_type)
        plus_up = store_plus_up(passenger_type, self.pcc)
        plus_up = plus_up if plus_up else ""
        fare_type_value = ""
        penalty_info = get_penalty_info() if not t_designator else ""
        header = self.generate_header("Session", "OTA_AirPriceLLSRQ", token)
        return f"""<?xml version="1.0" encoding="UTF-8"?>
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
                {header}
                <soapenv:Body>
                    <OTA_AirPriceRQ Version="2.17.0" xmlns="http://webservices.sabre.com/sabreXML/2011/10" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                        <PriceRequestInformation Retain="true">
                        <OptionalQualifiers>
                            {commission}
                            <PricingQualifiers>
                                {fare_type_value}
                                {brands}
                                {t_designator}
                                {segment_numbers}
                                {name_select}
                                {pax_type}
                                {plus_up}
                                {penalty_info}
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
        segments_list = segments_to_cancel(segment)
        return f"""<?xml version="1.0" encoding="UTF-8"?>
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
               {header}
                <soapenv:Body>
                    <OTA_CancelRQ xmlns="http://webservices.sabre.com/sabreXML/2011/10" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" NumResponses="1" ReturnHostCommand="false" TimeStamp="2016-05-17T10:00:00-06:00" Version="2.0.2">
                        {segments_list}
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
                                                 p_update.first_name, p_update.last_name, p_update.issue_country, p_update.known_traveler_number) if (p_update.date_of_birth and p_update.gender and p_update.first_name and p_update.last_name) or (p_update.known_traveler_number and p_update.issue_country and p_update.first_name and p_update.last_name) else ""
            service_ssr_part = service_ssr_code(p_update.segment_number, p_update.ssr_code, p_update.name_number) if p_update.segment_number and p_update.ssr_code else ""
        else:
            seat_part, passenger_info_part, service_ssr_part = ("", "", "")

        # dk_number_part = customer_id(p_update.dk_number) if p_update.dk_number else ""
        travel_itinerary_add_info_request = travel_itinerary_add_info_rq(dk_number=p_update.dk_number, member_ship_id=p_update.member_ship_id, name_number=p_update.name_number, program_id=p_update.program_id, segment_number=p_update.segment_number)
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
                            {travel_itinerary_add_info_request}
                    </PassengerDetailsRQ>
                </soapenv:Body>
            </soapenv:Envelope>"""

    def approval_code_info(self, approval_code):
        if approval_code is not None:
            return f"""ManualApprovalCode = "{approval_code}" """
        else:
            return ""

    def info_credit_card(self, code_cc, expire_date, cc_number, approval_code):
        return f"""<FOP_Qualifiers>
                    <BasicFOP>
                        <CC_Info Suppress="true">
                            <PaymentCard Code="{code_cc}" ExpireDate="{expire_date}" {self.approval_code_info(approval_code)} Number="{cc_number}"/>
                        </CC_Info>
                    </BasicFOP>
                </FOP_Qualifiers>"""

    def info_cash_or_cheque(self, payment_type):
        return f"""<FOP_Qualifiers>
                    <BasicFOP Type="{payment_type}"/>
                </FOP_Qualifiers>"""

    def seap_map_rq(self, token, flight_infos: FlightSeatMap, passengers_info: List[Passenger]):
        """
            Return the xml request to search a seap map
        """
        header = self.generate_header("EnhancedSeatMapRQ", "EnhancedSeatMapRQ", token)
        flight_info = add_flight_segment(flight_infos.origin, flight_infos.destination, flight_infos.depart_date, flight_infos.operating_code, flight_infos.operating_flight_number, flight_infos.marketing_code, flight_infos.marketing_flight_number, flight_infos.arrival_date, flight_infos.class_of_service, flight_infos.currency_code)
        pax_info = add_passenger_info(passengers_info)
        return f"""<?xml version="1.0" encoding="UTF-8"?>
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
               {header}
                <soapenv:Body>
                    <tag0:EnhancedSeatMapRQ xmlns:tag0="http://stl.sabre.com/Merchandising/v6" version="6">
                        <tag0:RequestType>Payload</tag0:RequestType>
                        <tag0:SeatMapQueryEnhanced correlationID="20190218103518">
                                {flight_info}
                                {pax_info}
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

    def exchange_shopping_rq(self, token: str, pnr: str, passengers: List[dict], origin_destination: List[dict]):
        """ Return the xml request to search for available flights for a ticket number to be exchanged

        Arguments:
            token {str} -- the security token
            pnr {str} -- the pnr code

        Keyword Arguments:
            passengers {list} -- list of passengers information (default: {[dict]})
            origin_destination {list} -- list of itineraries information (default: {[dict]})

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
                            {get_passengers_in_exchange_shopping(pnr, passengers)}
                        </PassengerInformation>
                            {get_segments_in_exchange_shopping(origin_destination)}
                    </ExchangeShoppingRQ>
                </soapenv:Body>
            </soapenv:Envelope>"""

    def automated_exchanges_price_rq(self, token: str, ticket_number: str, name_number: str, passenger_type: str, markup: float = 0.0):
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
                                        {get_markup_exchange_price(markup)}
                                    </PricingQualifiers>
                                </OptionalQualifiers>
                            </PriceRequestInformation>
                        </ExchangeComparison>
                    </AutomatedExchangesRQ>
                </soapenv:Body>
            </soapenv:Envelope>"""

    def automated_exchanges_commmit_rq(self, token: str, price_quote: int, form_of_payment: FormOfPayment):
        """
            Return the xml request to store a price
            for a ticket number to be exchanged
        """
        header = self.generate_header("AutomatedExchangesLLSRQ", "AutomatedExchangesLLSRQ", token)
        return f"""<?xml version="1.0" encoding="UTF-8"?>
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
                {header}
                <soapenv:Body>
                    <AutomatedExchangesRQ xmlns="http://webservices.sabre.com/sabreXML/2011/10" ReturnHostCommand="true" Version="2.7.0">
                        <ExchangeConfirmation PQR_Number="{price_quote}">
                            <OptionalQualifiers>
                                {self.fop_choice(form_of_payment)}
                            </OptionalQualifiers>
                        </ExchangeConfirmation>
                    </AutomatedExchangesRQ>
                </soapenv:Body>
            </soapenv:Envelope>"""

    def ticketing_exchange_rq(self, token: str, price_quote: int):
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

    def send_remark_rq(self, token, text, remark_type):
        """
            Return the xml request to add a remark for a pnr
        """
        header = self.generate_header("PassengerDetailsRQ", "PassengerDetailsRQ", token)

        return f"""<?xml version="1.0" encoding="UTF-8"?>
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
                {header}
                <soapenv:Body>
                    <PassengerDetailsRQ haltOnError="true" ignoreOnError="false" xmlns="http://services.sabre.com/sp/pd/v3_4" version="3.4.0">
                        <PostProcessing unmaskCreditCard="true" ignoreAfter="false">
                        </PostProcessing>
                        <SpecialReqDetails>
                            <AddRemarkRQ>
                                <RemarkInfo>
                                    <Remark Type="{remark_type}">
                                        <Text>{text}</Text>
                                    </Remark>
                                </RemarkInfo>
                            </AddRemarkRQ>
                        </SpecialReqDetails>
                    </PassengerDetailsRQ>
                </soapenv:Body>
            </soapenv:Envelope>"""

    def fop_choice(self, fop: FormOfPayment):
        if not fop or fop.is_valid() is False:
            return ""
        if isinstance(fop, CreditCard):
            return self.info_credit_card(fop.vendor_code, fop.expiry_date, fop.card_number, fop.approval_code)
        else:
            return self.info_cash_or_cheque(fop.p_type)
        return ""

    def get_commission_value(self, fare_type, commission_percentage, markup):

        TWOPLACES = Decimal(10) ** -2
        if commission_percentage is not None and commission_percentage >= 0 and fare_type == "PUB":
            return f"""<MiscQualifiers>
                    <Commission Percent="{Decimal(commission_percentage).quantize(TWOPLACES)}"/>
                </MiscQualifiers>"""
        elif markup is not None and markup >= 0 and fare_type == "NET":
            return f"""<MiscQualifiers>
                    <Commission Amount="{Decimal(markup).quantize(TWOPLACES)}"/>
                </MiscQualifiers>"""
        return ""

    def get_name_select(self, name_select=None):

        return f"""<NameSelect NameNumber="{name_select}"/>""" if name_select else ""

    def air_ticket_rq(self, token_value, price_quote, form_of_payment: FormOfPayment, fare_type, commission_percentage, markup, name_select):
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
                                {self.fop_choice(form_of_payment)}
                                {self.get_commission_value(fare_type, commission_percentage, markup)}
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

    def price_quote_services_rq(self, token: str, record_locator: str):
        """ Return the xml request to display pricing information stored
        in the PNRs of Price Quote and Price Quote Reissue records

        Arguments:
            token {[str]} -- The security token
            record_locator {[str]} -- the record locator

        Returns:
            [str] -- price quote request
        """

        header = self.generate_header("PriceQuoteServicesRQ", "PriceQuoteServicesRQ", token)
        return f"""<?xml version="1.0" encoding="UTF-8"?>
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
                {header}
                <soapenv:Body>
                    <GetPriceQuoteRQ version="4.1.0" xmlns="http://www.sabre.com/ns/Ticketing/pqs/1.0">
                        <SearchParameters resultType="D">
                            <PriceQuoteInfo>
                            <Reservation>{record_locator}</Reservation>
                            <PriceQuote/>
                            </PriceQuoteInfo>
                        </SearchParameters>
                    </GetPriceQuoteRQ>
                </soapenv:Body>
            </soapenv:Envelope>"""
