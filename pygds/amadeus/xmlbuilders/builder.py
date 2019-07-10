from time import gmtime, strftime

from pygds.core.types import TravellerNumbering
from ..security_utils import generate_random_message_id, generate_created, generate_nonce, password_digest


class AmadeusXMLBuilder:
    """
    This class is for generating the needed XML for SOAP requests
    """

    def __init__(self, endpoint, username, password, office_id, wsap):
        self.current_timestamp = str(strftime("%Y-%m-%dT%H:%M:%S", gmtime()))
        self.endpoint = endpoint
        self.username = username
        self.password = password
        self.wsap = wsap
        self.office_id = office_id
        self.created_date_time = generate_created()
        self.nonce = generate_nonce()
        self.digested_password = password_digest(password, self.nonce, self.created_date_time)

    def ensure_security_parameters(self, message_id, nonce, created_date_time):
        """
            This method, ensures that security parameters are correct. Unless it generate them.
        """
        if created_date_time is None:
            created_date_time = generate_created()

        if message_id is None:
            message_id = generate_random_message_id()

        if nonce is None:
            nonce = generate_nonce()
        digested_password = password_digest(self.password, nonce, created_date_time)
        return (message_id, nonce, created_date_time, digested_password)

    def new_transaction_chunk(self, office_id, username, nonce, digested_password, created_date_time):
        """
            This method generates a chunk XML part for every endpoint that starts a new transaction.
        """
        return f"""
        <oas:Security xmlns:oas="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" xmlns:oas1="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">
            <oas:UsernameToken oas1:Id="UsernameToken-1">
                <oas:Username>{username}</oas:Username>
                <oas:Nonce EncodingType="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-soap-message-security-1.0#Base64Binary">{nonce}</oas:Nonce>
                <oas:Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordDigest">{digested_password}</oas:Password>
                <oas1:Created>{created_date_time}</oas1:Created>
            </oas:UsernameToken>
        </oas:Security>
        <AMA_SecurityHostedUser xmlns="http://xml.amadeus.com/2010/06/Security_v1">
            <UserID AgentDutyCode="SU" RequestorType="U" PseudoCityCode="{office_id}" POS_Type="1"/>
        </AMA_SecurityHostedUser>
       """

    def continue_transaction_chunk(self, session_id, sequence_number, security_token):
        """
            This method generates a chunk XML part for every endpoint that continues a transaction
        """
        return f"""
        <awsse:Session TransactionStatusCode="InSeries" xmlns:awsse="http://xml.amadeus.com/2010/06/Session_v3">
            <awsse:SessionId>{session_id}</awsse:SessionId>
            <awsse:SequenceNumber>{sequence_number}</awsse:SequenceNumber>
            <awsse:SecurityToken>{security_token}</awsse:SecurityToken>
        </awsse:Session>"""

    def start_transaction(self, message_id, office_id, username, password, nonce, created_date_time):
        """
            Example
        AmadeusXMLBuilder().start_transaction("WbsConsu-w5D0dntND8rNwtYwxewE5AdIsEJYqx9-vc69HKdaM", "DTW1S210B", "WSCSOCTS", "KsU6KnFHNIV8zcVoZC8ZYQ==", "mBzu72QJUIWMrdWW63dTpfj8HxY=",, "2017-05-29T14:44:41.457Z")
        """
        message_id, nonce, created_date_time, digested_password = self.ensure_security_parameters(message_id, nonce,
                                                                                                  created_date_time)
        security_part = self.new_transaction_chunk(office_id, username, nonce, digested_password, created_date_time)

        return f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:sec="http://xml.amadeus.com/2010/06/Security_v1" xmlns:typ="http://xml.amadeus.com/2010/06/Types_v1" xmlns:iat="http://www.iata.org/IATA/2007/00/IATA2010.1" xmlns:app="http://xml.amadeus.com/2010/06/AppMdw_CommonTypes_v3" xmlns:link="http://wsdl.amadeus.com/2010/06/ws/Link_v1" xmlns:ses="http://xml.amadeus.com/2010/06/Session_v3" xmlns:vls="http://xml.amadeus.com/VLSSOQ_04_1_1A">
            <soapenv:Header xmlns:add="http://www.w3.org/2005/08/addressing">
                <add:MessageID>{message_id}</add:MessageID>
                <add:Action>http://webservices.amadeus.com/VLSSOQ_04_1_1A</add:Action>
                <add:To>{self.endpoint}/{self.wsap}</add:To>
                {security_part}
            </soapenv:Header>
            <soapenv:Body>
                <vls:Security_SignOut/>
            </soapenv:Body>
        </soapenv:Envelope>
        """

    def end_transaction(self, message_id, session_id, sequence_number, security_token):
        return f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:sec="http://xml.amadeus.com/2010/06/Security_v1" xmlns:typ="http://xml.amadeus.com/2010/06/Types_v1" xmlns:iat="http://www.iata.org/IATA/2007/00/IATA2010.1" xmlns:app="http://xml.amadeus.com/2010/06/AppMdw_CommonTypes_v3" xmlns:link="http://wsdl.amadeus.com/2010/06/ws/Link_v1" xmlns:ses="http://xml.amadeus.com/2010/06/Session_v3" xmlns:vls="http://xml.amadeus.com/VLSSOQ_04_1_1A">
            <soapenv:Header xmlns:add="http://www.w3.org/2005/08/addressing">
                <add:MessageID>{message_id}</add:MessageID>
                <add:Action>http://webservices.amadeus.com/VLSSOQ_04_1_1A</add:Action>
                <add:To>{self.endpoint}/{self.wsap}</add:To>
                <awsse:Session TransactionStatusCode="End" xmlns:awsse="http://xml.amadeus.com/2010/06/Session_v3">
                    <awsse:SessionId>{session_id}</awsse:SessionId>
                    <awsse:SequenceNumber>{sequence_number}</awsse:SequenceNumber>
                    <awsse:SecurityToken>{security_token}</awsse:SecurityToken>
                </awsse:Session>
            </soapenv:Header>
            <soapenv:Body>
                <Security_SignOut></Security_SignOut>
            </soapenv:Body>
        </soapenv:Envelope>
        """

    def getReservationRQ(self, office_id, message_id, token, pnr_number, new_session=True):
        """
        Create XML request body for SOAP Operation getReservation. We use a given endpoint
        """
        # if message_id is None:
        #     message_id = generate_random_message_id("GETPNR-")
        # if new_session:
        #     status_session = "Start"
        #     security_part = self.new_transaction_chunk(self.username, self.nonce, self.digested_password)
        # else:
        #     status_session = "InSeries"
        #     security_part = self.continue_transaction_chunk("", "", token)

        return f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:sec="http://xml.amadeus.com/2010/06/Security_v1" xmlns:typ="http://xml.amadeus.com/2010/06/Types_v1" xmlns:iat="http://www.iata.org/IATA/2007/00/IATA2010.1" xmlns:app="http://xml.amadeus.com/2010/06/AppMdw_CommonTypes_v3" xmlns:link="http://wsdl.amadeus.com/2010/06/ws/Link_v1" xmlns:ses="http://xml.amadeus.com/2010/06/Session_v3">
            <soapenv:Header xmlns:add="http://www.w3.org/2005/08/addressing">
                <add:MessageID>{message_id}</add:MessageID>
                <add:Action>http://webservices.amadeus.com/PNRRET_17_1_1A</add:Action>
                <add:To>{self.endpoint}/{self.wsap}</add:To>
                <oas:Security xmlns:oas="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" xmlns:oas1="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">
                    <oas:UsernameToken oas1:Id="UsernameToken-1">
                        <oas:Username>{self.username}</oas:Username>
                        <oas:Nonce EncodingType="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-soap-message-security-1.0#Base64Binary">{self.nonce}</oas:Nonce>
                        <oas:Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordDigest">{self.digested_password}</oas:Password>
                        <oas1:Created>{self.created_date_time}</oas1:Created>
                    </oas:UsernameToken>
                </oas:Security>
                <AMA_SecurityHostedUser xmlns="http://xml.amadeus.com/2010/06/Security_v1">
                    <UserID AgentDutyCode="SU" RequestorType="U" PseudoCityCode="{office_id}" POS_Type="1"/>
                </AMA_SecurityHostedUser>
                <awsse:Session TransactionStatusCode="Start" xmlns:awsse="http://xml.amadeus.com/2010/06/Session_v3"/>
            </soapenv:Header>
            <soapenv:Body>
                <PNR_Retrieve>
                    <retrievalFacts>
                        <retrieve>
                        <type>2</type>
                        </retrieve>
                        <reservationOrProfileIdentifier>
                        <reservation>
                            <controlNumber>{pnr_number}</controlNumber>
                        </reservation>
                        </reservationOrProfileIdentifier>
                    </retrievalFacts>
                </PNR_Retrieve>
            </soapenv:Body>
        </soapenv:Envelope>
        """

    def fare_master_pricer_travel_board_search(self, office_id, origin, destination, departure_date, arrival_date, traveller_numbering: TravellerNumbering, result_count=250):
        """
            Search prices for origin/destination and departure/arrival dates
        """
        message_id, nonce, created_date_time, digested_password = self.ensure_security_parameters(None, None, None)
        security_part = self.new_transaction_chunk(self.office_id, self.username, nonce, digested_password,
                                                   created_date_time)
        return f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:sec="http://xml.amadeus.com/2010/06/Security_v1" xmlns:typ="http://xml.amadeus.com/2010/06/Types_v1" xmlns:iat="http://www.iata.org/IATA/2007/00/IATA2010.1" xmlns:app="http://xml.amadeus.com/2010/06/AppMdw_CommonTypes_v3" xmlns:link="http://wsdl.amadeus.com/2010/06/ws/Link_v1" xmlns:ses="http://xml.amadeus.com/2010/06/Session_v3">
            <soapenv:Header xmlns:add="http://www.w3.org/2005/08/addressing">
                <add:MessageID>{message_id}</add:MessageID>
                <add:Action>http://webservices.amadeus.com/FMPTBQ_18_1_1A</add:Action>
                <add:To>{self.endpoint}/{self.wsap}</add:To>
                {security_part}
            </soapenv:Header>
            <soapenv:Body>
                <Fare_MasterPricerTravelBoardSearch>
                    <numberOfUnit>
                        <unitNumberDetail>
                            <numberOfUnits>{traveller_numbering.total_seats()}</numberOfUnits>
                            <typeOfUnit>PX</typeOfUnit>
                        </unitNumberDetail>
                        <unitNumberDetail>
                            <numberOfUnits>{result_count}</numberOfUnits>
                            <typeOfUnit>RC</typeOfUnit>
                        </unitNumberDetail>
                    </numberOfUnit>
                    {self.generate_seat_traveller_numbering(traveller_numbering)}
                    <fareOptions>
                        <pricingTickInfo>
                        <pricingTicketing>
                            <priceType>ET</priceType>
                            <priceType>RP</priceType>
                            <priceType>RU</priceType>
                            <priceType>TAC</priceType>
                        </pricingTicketing>
                        </pricingTickInfo>
                    </fareOptions>
                    <travelFlightInfo>
                        <flightDetail>
                        <flightType>N</flightType>
                        </flightDetail>
                    </travelFlightInfo>
                    <itinerary>
                        <requestedSegmentRef>
                        <segRef>1</segRef>
                        </requestedSegmentRef>
                        <departureLocalization>
                        <depMultiCity>
                            <locationId>{origin}</locationId>
                            <airportCityQualifier>C</airportCityQualifier>
                        </depMultiCity>
                        </departureLocalization>
                        <arrivalLocalization>
                        <arrivalMultiCity>
                            <locationId>{destination}</locationId>
                            <airportCityQualifier>C</airportCityQualifier>
                        </arrivalMultiCity>
                        </arrivalLocalization>
                        <timeDetails>
                        <firstDateTimeDetail>
                            <date>{departure_date}</date>
                        </firstDateTimeDetail>
                        <rangeOfDate>
                            <rangeQualifier>M</rangeQualifier>
                            <dayInterval>2</dayInterval>
                        </rangeOfDate>
                        </timeDetails>
                    </itinerary>
                    <itinerary>
                        <requestedSegmentRef>
                            <segRef>1</segRef>
                        </requestedSegmentRef>
                        <departureLocalization>
                            <depMultiCity>
                                <locationId>{destination}</locationId>
                                <airportCityQualifier>C</airportCityQualifier>
                            </depMultiCity>
                        </departureLocalization>
                        <arrivalLocalization>
                            <arrivalMultiCity>
                                <locationId>{origin}</locationId>
                                <airportCityQualifier>C</airportCityQualifier>
                            </arrivalMultiCity>
                        </arrivalLocalization>
                        <timeDetails>
                            <firstDateTimeDetail>
                                <date>{arrival_date}</date>
                            </firstDateTimeDetail>
                            <rangeOfDate>
                                <rangeQualifier>M</rangeQualifier>
                                <dayInterval>2</dayInterval>
                            </rangeOfDate>
                        </timeDetails>
                    </itinerary>

                </Fare_MasterPricerTravelBoardSearch>
            </soapenv:Body>
            </soapenv:Envelope>
        """

    def generate_seat_traveller_numbering(self, traveller_numbering: TravellerNumbering):
        adults = ""
        children = ""
        infants = ""
        if traveller_numbering.adults != 0:
            adults = self._traveler_ref("ADT", 1, traveller_numbering.adults)
        if traveller_numbering.children != 0:
            children = self._traveler_ref("CH", traveller_numbering.adults + 1, traveller_numbering.children)
        if traveller_numbering.infants != 0:
            infants = self._traveler_ref("INF", 1, traveller_numbering.infants)
        return f"""
        {adults}
        {children}
        {infants}
        """

    def _traveler_ref(self, pax_type, begin, pax_number):
        travellers = ""
        infant_indicator = ""
        if pax_type == 'INF':
            infant_indicator = "<infantIndicator>1</infantIndicator>"
        for ref in range(begin, begin + pax_number):
            travellers += f"""
            <traveller>
                <ref>{ref}</ref>
                {infant_indicator}
            </traveller>
            """
        return f"""
        <paxReference>
            <ptc>{pax_type}</ptc>
            {travellers}
        </paxReference>
        """

    def fare_price_pnr_with_booking_class(self, message_id, session_id, sequence_number, security_token):
        security_part = self.continue_transaction_chunk(session_id, sequence_number, security_token)
        return f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:sec="http://xml.amadeus.com/2010/06/Security_v1" xmlns:typ="http://xml.amadeus.com/2010/06/Types_v1" xmlns:iat="http://www.iata.org/IATA/2007/00/IATA2010.1" xmlns:app="http://xml.amadeus.com/2010/06/AppMdw_CommonTypes_v3" xmlns:link="http://wsdl.amadeus.com/2010/06/ws/Link_v1" xmlns:ses="http://xml.amadeus.com/2010/06/Session_v3">
            <soapenv:Header xmlns:add="http://www.w3.org/2005/08/addressing">
                <add:MessageID>{message_id}</add:MessageID>
                <add:Action>http://webservices.amadeus.com/TPCBRQ_18_1_1A</add:Action>
                <add:To>{self.endpoint}/{self.wsap}</add:To>
                {security_part}
            </soapenv:Header>
            <soapenv:Body>
                <Fare_PricePNRWithBookingClass>
                    <pricingOptionGroup>
                        <pricingOptionKey>
                        <pricingOptionKey>RP</pricingOptionKey>
                        </pricingOptionKey>
                    </pricingOptionGroup>
                    <pricingOptionGroup>
                        <pricingOptionKey>
                        <pricingOptionKey>RU</pricingOptionKey>
                        </pricingOptionKey>
                    </pricingOptionGroup>
                </Fare_PricePNRWithBookingClass>
            </soapenv:Body>
        </soapenv:Envelope>
        """

    def ticket_create_TST_from_price(self, message_id, session_id, sequence_number, security_token, tst_reference):
        security_part = self.continue_transaction_chunk(session_id, sequence_number, security_token)
        return f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:sec="http://xml.amadeus.com/2010/06/Security_v1" xmlns:typ="http://xml.amadeus.com/2010/06/Types_v1" xmlns:iat="http://www.iata.org/IATA/2007/00/IATA2010.1" xmlns:app="http://xml.amadeus.com/2010/06/AppMdw_CommonTypes_v3" xmlns:link="http://wsdl.amadeus.com/2010/06/ws/Link_v1" xmlns:ses="http://xml.amadeus.com/2010/06/Session_v3">
            <soapenv:Header xmlns:add="http://www.w3.org/2005/08/addressing">
                <add:MessageID>{message_id}</add:MessageID>
                <add:Action>http://webservices.amadeus.com/TAUTCQ_04_1_1A</add:Action>
                <add:To>{self.endpoint}/{self.wsap}</add:To>
                {security_part}
            </soapenv:Header>
            <soapenv:Body>
                <Ticket_CreateTSTFromPricing>
                    <psaList>
                        <itemReference>
                        <referenceType>TST</referenceType>
                        <uniqueReference>{tst_reference}</uniqueReference>
                        </itemReference>
                    </psaList>
                </Ticket_CreateTSTFromPricing>
            </soapenv:Body>
        </soapenv:Envelope>
        """

    def sell_from_recomendation(self, itineraries):
        message_id, nonce, created_date_time, digested_password = self.ensure_security_parameters(None, None, None)
        security_part = self.new_transaction_chunk(self.office_id, self.username, nonce, digested_password,
                                                   created_date_time)

        itineraries_details = []
        for it in itineraries:
            itineraries_details.append(
                self.itenerary_details(it.origin, it.destination, it.departure_date, it.company, it.flight_number,
                                       it.booking_class, it.quantity))
        return f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:sec="http://xml.amadeus.com/2010/06/Security_v1" xmlns:typ="http://xml.amadeus.com/2010/06/Types_v1" xmlns:iat="http://www.iata.org/IATA/2007/00/IATA2010.1" xmlns:app="http://xml.amadeus.com/2010/06/AppMdw_CommonTypes_v3" xmlns:link="http://wsdl.amadeus.com/2010/06/ws/Link_v1" xmlns:ses="http://xml.amadeus.com/2010/06/Session_v3">
            <soapenv:Header xmlns:add="http://www.w3.org/2005/08/addressing">
                <add:MessageID>{message_id}</add:MessageID>
                <add:Action>http://webservices.amadeus.com/ITAREQ_05_2_IA</add:Action>
                <add:To>{self.endpoint}/{self.wsap}</add:To>
                {security_part}
                <awsse:Session TransactionStatusCode="Start" xmlns:awsse="http://xml.amadeus.com/2010/06/Session_v3"/>
            </soapenv:Header>
            <soapenv:Body>
                <Air_SellFromRecommendation>
                    <messageActionDetails>
                        <messageFunctionDetails>
                        <messageFunction>183</messageFunction>
                        <additionalMessageFunction>M1</additionalMessageFunction>
                        </messageFunctionDetails>
                    </messageActionDetails>
                    {''.join(itineraries_details)}
                </Air_SellFromRecommendation>
            </soapenv:Body>
        </soapenv:Envelope>
        """

    def itenerary_details(self, origin, destination, departure_date, company, flight_number, booking_class, quantity):
        return f"""
        <itineraryDetails>
            <originDestinationDetails>
            <origin>{origin}</origin>
            <destination>{destination}</destination>
            </originDestinationDetails>
            <message>
            <messageFunctionDetails>
                <messageFunction>183</messageFunction>
            </messageFunctionDetails>
            </message>
            <segmentInformation>
            <travelProductInformation>
                <flightDate>
                    <departureDate>{departure_date}</departureDate>
                </flightDate>
                <boardPointDetails>
                    <trueLocationId>{origin}</trueLocationId>
                </boardPointDetails>
                <offpointDetails>
                    <trueLocationId>{destination}</trueLocationId>
                </offpointDetails>
                <companyDetails>
                    <marketingCompany>{company}</marketingCompany>
                </companyDetails>
                <flightIdentification>
                    <flightNumber>{flight_number}</flightNumber>
                    <bookingClass>{booking_class}</bookingClass>
                </flightIdentification>
            </travelProductInformation>
            <relatedproductInformation>
                <quantity>{quantity}</quantity>
                <statusCode>NN</statusCode>
            </relatedproductInformation>
            </segmentInformation>
        </itineraryDetails>
        """

    def add_passenger_info(self, office_id, message_id, session_id, sequence_number, security_token, infos):
        security_part = self.continue_transaction_chunk(session_id, sequence_number, security_token)
        passenger_infos = []
        for i in infos:
            passenger_infos.append(
                self.traveller_info(i.ref_number, i.first_name, i.surname, i.last_name, i.date_of_birth, i.pax_type))
        return f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:sec="http://xml.amadeus.com/2010/06/Security_v1" xmlns:typ="http://xml.amadeus.com/2010/06/Types_v1" xmlns:iat="http://www.iata.org/IATA/2007/00/IATA2010.1" xmlns:app="http://xml.amadeus.com/2010/06/AppMdw_CommonTypes_v3" xmlns:link="http://wsdl.amadeus.com/2010/06/ws/Link_v1" xmlns:ses="http://xml.amadeus.com/2010/06/Session_v3">
            <soapenv:Header xmlns:add="http://www.w3.org/2005/08/addressing">
                <add:MessageID>{message_id}</add:MessageID>
                <add:Action>http://webservices.amadeus.com/PNRADD_17_1_1A</add:Action>
                <add:To>{self.endpoint}/{self.wsap}</add:To>
                {security_part}
            </soapenv:Header>
            <soapenv:Body>
                <PNR_AddMultiElements>
                    <pnrActions>
                        <optionCode>0</optionCode>
                    </pnrActions>
                    {''.join(passenger_infos)}
                    <dataElementsMaster>
                        <marker1/>
                        <dataElementsIndiv>
                        <elementManagementData>
                            <segmentName>RF</segmentName>
                        </elementManagementData>
                        <freetextData>
                            <freetextDetail>
                                <subjectQualifier>3</subjectQualifier>
                                <type>P22</type>
                            </freetextDetail>
                            <longFreetext>{office_id}</longFreetext>
                        </freetextData>
                        </dataElementsIndiv>
                        <dataElementsIndiv>
                        <elementManagementData>
                            <segmentName>OP</segmentName>
                        </elementManagementData>
                        <optionElement>
                            <optionDetail>
                                <officeId>{office_id}</officeId>
                            </optionDetail>
                        </optionElement>
                        </dataElementsIndiv>
                        <dataElementsIndiv>
                        <elementManagementData>
                            <segmentName>AP</segmentName>
                        </elementManagementData>
                        <freetextData>
                            <freetextDetail>
                                <subjectQualifier>7</subjectQualifier>
                                <type>6</type>
                            </freetextDetail>
                            <longFreetext>0722541415</longFreetext>
                        </freetextData>
                        </dataElementsIndiv>
                        <dataElementsIndiv>
                        <elementManagementData>
                            <segmentName>AP</segmentName>
                        </elementManagementData>
                        <freetextData>
                            <freetextDetail>
                                <subjectQualifier>7</subjectQualifier>
                                <type>7</type>
                            </freetextDetail>
                            <longFreetext>0722541415</longFreetext>
                        </freetextData>
                        </dataElementsIndiv>
                        <dataElementsIndiv>
                        <elementManagementData>
                            <segmentName>AP</segmentName>
                        </elementManagementData>
                        <freetextData>
                            <freetextDetail>
                                <subjectQualifier>7</subjectQualifier>
                                <type>P02</type>
                            </freetextDetail>
                            <longFreetext>cjebelean@xvalue.ro</longFreetext>
                        </freetextData>
                        </dataElementsIndiv>
                        <dataElementsIndiv>
                        <elementManagementData>
                            <segmentName>TK</segmentName>
                        </elementManagementData>
                        <ticketElement>
                            <ticket>
                                <indicator>OK</indicator>
                            </ticket>
                        </ticketElement>
                        </dataElementsIndiv>
                        <dataElementsIndiv>
                        <elementManagementData>
                            <segmentName>FP</segmentName>
                        </elementManagementData>
                        <formOfPayment>
                            <fop>
                                <identification>CA</identification>
                            </fop>
                        </formOfPayment>
                        </dataElementsIndiv>
                        <dataElementsIndiv>
                        <elementManagementData>
                            <reference>
                                <qualifier>OT</qualifier>
                                <number>1</number>
                            </reference>
                            <segmentName>FM</segmentName>
                        </elementManagementData>
                        <commission>
                            <commissionInfo>
                                <percentage>5</percentage>
                            </commissionInfo>
                        </commission>
                        </dataElementsIndiv>
                    </dataElementsMaster>
                </PNR_AddMultiElements>
            </soapenv:Body>
        </soapenv:Envelope>
        """

    def traveller_info(self, ref_number, first_name, surname, last_name, date_of_birth, pax_type):
        return f"""
        <travellerInfo>
            <elementManagementPassenger>
            <reference>
                <qualifier>PR</qualifier>
                <number>{ref_number}</number>
            </reference>
            <segmentName>NM</segmentName>
            </elementManagementPassenger>
            <passengerData>
            <travellerInformation>
                <traveller>
                    <surname>{surname}</surname>
                    <quantity>1</quantity>
                </traveller>
                <passenger>
                    <firstName>{first_name}</firstName>
                    <type>{pax_type}</type>
                </passenger>
            </travellerInformation>
            <dateOfBirth>
                <dateAndTimeDetails>
                    <date>{date_of_birth}</date>
                </dateAndTimeDetails>
            </dateOfBirth>
            </passengerData>
        </travellerInfo>
        """
