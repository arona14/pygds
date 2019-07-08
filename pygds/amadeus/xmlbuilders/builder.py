from time import gmtime, strftime
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
        message_id, nonce, created_date_time, digested_password = self.ensure_security_parameters(message_id, nonce, created_date_time)
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

    def fare_master_pricer_travel_board_search(self, office_id, origin, destination, departure_date, arrival_date):
        """
            Search prices for origin/destination and departure/arrival dates
        """
        message_id, nonce, created_date_time, digested_password = self.ensure_security_parameters(None, None, None)
        security_part = self.new_transaction_chunk(self.office_id, self.username, nonce, digested_password, created_date_time)
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
                        <numberOfUnits>2</numberOfUnits>
                        <typeOfUnit>PX</typeOfUnit>
                        </unitNumberDetail>
                        <unitNumberDetail>
                        <numberOfUnits>100</numberOfUnits>
                        <typeOfUnit>RC</typeOfUnit>
                        </unitNumberDetail>
                    </numberOfUnit>
                    <paxReference>
                        <ptc>ADT</ptc>
                        <traveller>
                        <ref>1</ref>
                        </traveller>
                        <traveller>
                        <ref>2</ref>
                        </traveller>
                    </paxReference>
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
