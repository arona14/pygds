from time import gmtime, strftime
from typing import List
from pygds.amadeus.xmlbuilders import sub_parts
from pygds.core.price import PriceRequest
from pygds.core.sessions import SessionInfo
from pygds.core.types import TravellerNumbering, Itinerary
from pygds.core.request import LowFareSearchRequest
<<<<<<< HEAD
from pygds.core.payment import FormOfPayment, CreditCard, ChashPayment
=======
from pygds.core.payment import CreditCard
>>>>>>> 03ae67bb20447cd73e03eec553f9d9cb4c44a07a
from pygds.core.security_utils import generate_random_message_id, generate_created, generate_nonce, password_digest


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
        return message_id, nonce, created_date_time, digested_password

    def new_transaction_chunk(self, office_id, username, nonce, digested_password, created_date_time,
                              close_trx: bool = False):
        """
        This method generates a chunk XML part for every endpoint that starts a new transaction.
        :param office_id: The office id
        :param username: The usernme
        :param nonce: The nonce
        :param digested_password: The password digested
        :param created_date_time: The created date time
        :param close_trx: close or not the transaction
        :return: a str containing the XML part
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
        </AMA_SecurityHostedUser>{'' if close_trx else '<ses:Session xmlns:ses="http://xml.amadeus.com/2010/06/Session_v3" TransactionStatusCode="Start" />'}
       """

    def continue_transaction_chunk(self, session_id, sequence_number, security_token, close_trx: bool = False):
        """
            This method generates a chunk XML part for every endpoint that continues a transaction
        """
        return f"""
            <awsse:Session TransactionStatusCode="{'End' if close_trx else 'InSeries'}" xmlns:awsse="http://xml.amadeus.com/2010/06/Session_v3">
                <awsse:SessionId>{session_id}</awsse:SessionId>
                <awsse:SequenceNumber>{sequence_number}</awsse:SequenceNumber>
                <awsse:SecurityToken>{security_token}</awsse:SecurityToken>
            </awsse:Session>"""

    def generate_header(self, action, message_id, session_id, sequence_number, security_token, close_trx: bool = False):
        """
        This method generates the security part in SAOP Header.
        :param action: The Amadeus Soap Action code (without the whole URL)
        :param message_id: The message Id
        :param session_id: str the session id when continuing the transaction
        :param sequence_number: the sequence number when continuing the transaction
        :param security_token:
        :param close_trx:
        :return:
        """
        security = None
        if session_id is None:
            message_id, nonce, dt, dp = self.ensure_security_parameters(None, None, None)
            security = self.new_transaction_chunk(self.office_id, self.username, nonce, dp, dt, close_trx)
        else:
            security = self.continue_transaction_chunk(session_id, sequence_number, security_token, close_trx)
        return f"""
            <soapenv:Header xmlns:add="http://www.w3.org/2005/08/addressing">
                <add:MessageID>{message_id}</add:MessageID>
                <add:Action>http://webservices.amadeus.com/{action}</add:Action>
                <add:To>{self.endpoint}/{self.wsap}</add:To>
                {security}
            </soapenv:Header>"""

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
                <add:Action>http://webservices.amadeus.com/VLSSLQ_06_1_1A</add:Action>
                <add:To>{self.endpoint}/{self.wsap}</add:To>
                {security_part}
            </soapenv:Header>
            <soapenv:Body>
                <Security_Authenticate xmlns="http://xml.amadeus.com/VLSSLQ_06_1_1A" >
                    <userIdentifier>
                        <originatorTypeCode>U</originatorTypeCode>
                        <originator>{self.username}</originator>
                    </userIdentifier>
                    <dutyCode>
                        <dutyCodeDetails>
                            <referenceQualifier>DUT</referenceQualifier>
                            <referenceIdentifier>SU</referenceIdentifier>
                        </dutyCodeDetails>
                    </dutyCode>
                </Security_Authenticate>
            </soapenv:Body>
        </soapenv:Envelope>
        """

    def end_session(self, message_id, session_id, sequence_number, security_token):
        """

        """
        header = self.generate_header("VLSSOQ_04_1_1A", message_id, session_id, sequence_number, security_token, True)
        return f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:sec="http://xml.amadeus.com/2010/06/Security_v1" xmlns:typ="http://xml.amadeus.com/2010/06/Types_v1" xmlns:iat="http://www.iata.org/IATA/2007/00/IATA2010.1" xmlns:app="http://xml.amadeus.com/2010/06/AppMdw_CommonTypes_v3" xmlns:link="http://wsdl.amadeus.com/2010/06/ws/Link_v1" xmlns:ses="http://xml.amadeus.com/2010/06/Session_v3" xmlns:vls="http://xml.amadeus.com/VLSSOQ_04_1_1A">
            {header}
            <soapenv:Body>
                <Security_SignOut></Security_SignOut>
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

    def get_reservation_builder(self, pnr_number: str, message_id: str = None, session_id: str = None,
                                sequence_number: str = None, security_token: str = None, close_trx: bool = False):
        """
            Create XML request body for SOAP Operation getReservation. We use a given endpoint
        """
        return f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:sec="http://xml.amadeus.com/2010/06/Security_v1" xmlns:typ="http://xml.amadeus.com/2010/06/Types_v1" xmlns:iat="http://www.iata.org/IATA/2007/00/IATA2010.1" xmlns:app="http://xml.amadeus.com/2010/06/AppMdw_CommonTypes_v3" xmlns:link="http://wsdl.amadeus.com/2010/06/ws/Link_v1" xmlns:ses="http://xml.amadeus.com/2010/06/Session_v3">
             {self.generate_header("PNRRET_17_1_1A", message_id, session_id, sequence_number, security_token,
                                   close_trx)}
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

    def fare_master_pricer_travel_board_search(self, office_id, low_fare_search: LowFareSearchRequest, currency_conversion=None, c_qualifier="RC", with_stops=True, result_count=50):
        """
            Search prices for origin/destination and departure/arrival dates
        """
        message_id, nonce, created_date_time, digested_password = self.ensure_security_parameters(None, None, None)
        security_part = self.new_transaction_chunk(self.office_id, self.username, nonce, digested_password,
                                                   created_date_time)
        # currency_conversion: str = None
        stop_option = ""
        if not with_stops:
            stop_option = """
            <travelFlightInfo>
                <flightDetail>
                    <flightType>N</flightType>
                </flightDetail>
            </travelFlightInfo>
            """
        pricing_options = ["ET", "RP", "RU", "TAC"]
        # carrierid_options = ["DL", "AF"]
        # type_com: str = None
        # if type_com:
        #     pricing_options.append("RW")
        # identify = "012345"
        if currency_conversion:
            pricing_options.append("CUC")
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
                            <numberOfUnits>{low_fare_search.travelingNumber.total_seats()}</numberOfUnits>
                            <typeOfUnit>PX</typeOfUnit>
                        </unitNumberDetail>
                        <unitNumberDetail>
                            <numberOfUnits>{result_count}</numberOfUnits>
                            <typeOfUnit>RC</typeOfUnit>
                        </unitNumberDetail>
                    </numberOfUnit>
                    {sub_parts.generate_seat_traveller_numbering(low_fare_search.travelingNumber)}
                    <fareOptions>
                        <pricingTickInfo>
                            {sub_parts.mptbs_pricing_types(pricing_options)}
                        </pricingTickInfo>
                        {sub_parts.mptbs_currency_conversion(currency_conversion)}
                    </fareOptions>
                    {sub_parts.travel_flight_info(low_fare_search, c_qualifier)}
                    {stop_option}
                    {''.join([sub_parts.mptbs_itinerary(segment) for segment in low_fare_search.itineraries])}
            </Fare_MasterPricerTravelBoardSearch>
            </soapenv:Body>
            </soapenv:Envelope>
        """

    def fare_informative_price_without_pnr(self, message_id, session_id, sequence_number,
                                           security_token, numbering: TravellerNumbering, itineraries: List[Itinerary]):
        header = self.generate_header("TIPNRQ_18_1_1A", message_id, session_id, sequence_number, security_token)

        return f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:sec="http://xml.amadeus.com/2010/06/Security_v1" xmlns:typ="http://xml.amadeus.com/2010/06/Types_v1" xmlns:iat="http://www.iata.org/IATA/2007/00/IATA2010.1" xmlns:app="http://xml.amadeus.com/2010/06/AppMdw_CommonTypes_v3" xmlns:link="http://wsdl.amadeus.com/2010/06/ws/Link_v1" xmlns:ses="http://xml.amadeus.com/2010/06/Session_v3">
           {header}
           <soapenv:Body>
              <Fare_InformativePricingWithoutPNR>
                 {sub_parts.fare_informative_price_passengers(numbering)}
                 {sub_parts.fare_informative_price_segments(itineraries)}
              </Fare_InformativePricingWithoutPNR>
            </soapenv:Body>
        </soapenv:Envelope>
        """

    def fare_check_rules(self, message_id, session_id, sequence_number,
                         security_token, line_number):
        header = self.generate_header("FARQNQ_07_1_1A", message_id, session_id, sequence_number, security_token)
        return f"""
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
            xmlns:sec="http://xml.amadeus.com/2010/06/Security_v1"
            xmlns:typ="http://xml.amadeus.com/2010/06/Types_v1"
            xmlns:iat="http://www.iata.org/IATA/2007/00/IATA2010.1"
            xmlns:app="http://xml.amadeus.com/2010/06/AppMdw_CommonTypes_v3"
            xmlns:link="http://wsdl.amadeus.com/2010/06/ws/Link_v1"
            xmlns:ses="http://xml.amadeus.com/2010/06/Session_v3">
            {header}
            <soapenv:Body>
                    <Fare_CheckRules>
                        <msgType>
                            <messageFunctionDetails>
                            <messageFunction>712</messageFunction>
                            </messageFunctionDetails>
                        </msgType>
                        <itemNumber>
                            <itemNumberDetails>
                            <number>{line_number}</number>
                            </itemNumberDetails>
                        </itemNumber>
                    </Fare_CheckRules>
            </soapenv:Body>
        </soapenv:Envelope>"""

    def fare_price_pnr_with_booking_class(self, message_id, session_id, sequence_number, security_token,
                                          price_request: PriceRequest):
        header = self.generate_header("TPCBRQ_18_1_1A", message_id, session_id, sequence_number, security_token)
        return f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
            xmlns:sec="http://xml.amadeus.com/2010/06/Security_v1"
            xmlns:typ="http://xml.amadeus.com/2010/06/Types_v1"
            xmlns:iat="http://www.iata.org/IATA/2007/00/IATA2010.1"
            xmlns:app="http://xml.amadeus.com/2010/06/AppMdw_CommonTypes_v3"
            xmlns:link="http://wsdl.amadeus.com/2010/06/ws/Link_v1"
            xmlns:ses="http://xml.amadeus.com/2010/06/Session_v3">
            {header}
            <soapenv:Body>
                <Fare_PricePNRWithBookingClass>
                    {sub_parts.ppwbc_fare_type(price_request.fare_type)}
                    {sub_parts.ppwbc_passenger_segment_selection(price_request)}
                </Fare_PricePNRWithBookingClass>
            </soapenv:Body>
        </soapenv:Envelope>
        """

    def ticket_create_tst_from_price(self, message_id, session_id, sequence_number, security_token, tst_reference):
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

    def create_pnr(self, message_id, session_id, sequence_number, security_token):
        security_part = self.continue_transaction_chunk(session_id, sequence_number, security_token)
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
                                <optionCode>10</optionCode>
                                <optionCode>30</optionCode>
                            </pnrActions>
                        </PNR_AddMultiElements>
                    </soapenv:Body>
                </soapenv:Envelope>
                """

    def sell_from_recomendation(self, message_id, session_id, sequence_number,
                                security_token, itineraries):

        header = self.generate_header("ITAREQ_05_2_IA", message_id, session_id, sequence_number, security_token)

        itineraries_details = []
        for it in itineraries:
            # itineraries_details.append(sub_parts.sell_from_recommendation_itinerary_details(it.origin, it.destination, it.segments))
            itineraries_details.append(
                self.itenerary_details(it.origin, it.destination, it.departure_date, it.company, it.flight_number,
                                       it.booking_class, it.quantity))
        # The optimization algorithm. M1: cancel all if unsuccessful, M2: keep all confirmed if unsuccessful
        algo = 'M1'
        return f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:sec="http://xml.amadeus.com/2010/06/Security_v1" xmlns:typ="http://xml.amadeus.com/2010/06/Types_v1" xmlns:iat="http://www.iata.org/IATA/2007/00/IATA2010.1" xmlns:app="http://xml.amadeus.com/2010/06/AppMdw_CommonTypes_v3" xmlns:link="http://wsdl.amadeus.com/2010/06/ws/Link_v1" xmlns:ses="http://xml.amadeus.com/2010/06/Session_v3">
            {header}
            <soapenv:Body>
                <Air_SellFromRecommendation>
                    <messageActionDetails>
                        <messageFunctionDetails>
                        <messageFunction>183</messageFunction>
                        <additionalMessageFunction>{algo}</additionalMessageFunction>
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
        for i in infos.traveller_info:
            passenger_infos.append(
                sub_parts.add_multi_elements_traveller_info(i.ref_number, i.first_name, i.surname, i.last_name,
                                                            i.date_of_birth, i.pax_type))
        # type = 6 Travel agent telephone number
        # type = PO2 E-mail address
        # type = 7 Mobile Phone Number
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
                        {sub_parts.add_multi_element_data_element("RF", 3, "P22", office_id)}
                        <dataElementsIndiv>
                            <elementManagementData>
                                <segmentName>OP</segmentName>
                            </elementManagementData>
                            <optionElement>
                                <optionDetail>
                                    <officeId>{office_id if office_id is not None else ""}</officeId>
                                </optionDetail>
                            </optionElement>
                        </dataElementsIndiv>
                        {sub_parts.add_multi_element_contact_element("7", infos.number_tel) if infos.number_tel else ""}
                        {sub_parts.add_multi_element_contact_element("6", infos.number_tel_agent) if infos.number_tel else ""}
                        {sub_parts.add_multi_element_contact_element("P02", infos.email) if infos.number_tel else ""}
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

    def send_command(self, command: str, message_id: str = None, session_id: str = None, sequence_number: str = None,
                     security_token: str = None, close_trx: bool = False):
        return f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:sec="http://xml.amadeus.com/2010/06/Security_v1" xmlns:typ="http://xml.amadeus.com/2010/06/Types_v1" xmlns:iat="http://www.iata.org/IATA/2007/00/IATA2010.1" xmlns:app="http://xml.amadeus.com/2010/06/AppMdw_CommonTypes_v3" xmlns:link="http://wsdl.amadeus.com/2010/06/ws/Link_v1" xmlns:ses="http://xml.amadeus.com/2010/06/Session_v3">
            {self.generate_header("HSFREQ_07_3_1A", message_id, session_id, sequence_number, security_token, close_trx)}
            <soapenv:Body>
                <Command_Cryptic>
                    <messageAction>
                        <messageFunctionDetails>
                            <messageFunction>M</messageFunction>
                        </messageFunctionDetails>
                    </messageAction>
                    <longTextString>
                        <textStringDetails>{command}</textStringDetails>
                    </longTextString>
                </Command_Cryptic>
            </soapenv:Body>
        </soapenv:Envelope>
        """

    def add_form_of_payment_builder(self, message_id, session_id, sequence_number, security_token, form_of_payment,
                                    passenger_reference_type, passenger_reference_value,
                                    form_of_payment_sequence_number,
                                    group_usage_attribute_type, fop: CreditCard):
        security_part = self.continue_transaction_chunk(session_id, sequence_number, security_token)

        form_of_payment_code = fop.p_code
        company_code = fop.company_code
        form_of_payment_type = fop.p_type
<<<<<<< HEAD
        group_usage_attribute_type = "FP"  # "PAY"
        form_of_payment = "FP"  # "DEF
        pax_refs = pax_refs or []
        inf_refs = inf_refs or []
        segment_refs = segment_refs or []

        if isinstance(fop, CreditCard):
            return f"""
                <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                    xmlns:sec="http://xml.amadeus.com/2010/06/Security_v1"
                    xmlns:link="http://wsdl.amadeus.com/2010/06/ws/Link_v1"
                    xmlns:ses="http://xml.amadeus.com/2010/06/Session_v3"
                    xmlns:tfop="http://xml.amadeus.com/TFOPCQ_15_4_1A">
                {self.generate_header("TFOPCQ_15_4_1A", message_id, session_id, sequence_number, security_token, False)}
                <soapenv:Body>
                    <FOP_CreateFormOfPayment>
                        <transactionContext>
                            <transactionDetails>
                                <code>{form_of_payment}</code>
                            </transactionDetails>
                        </transactionContext>
                        <fopGroup>
                            <fopReference></fopReference>
                            {"".join([sub_parts.fop_passenger("PAX", ref) for ref in pax_refs])}
                            {"".join([sub_parts.fop_passenger("INF", ref) for ref in inf_refs])}
                            {"".join([sub_parts.fop_segment(ref) for ref in segment_refs])}
                            <mopDescription>
                            {sub_parts.fop_sequence_number(fop_sequence_number) if fop_sequence_number else ""}
                            <mopDetails>
                                <fopPNRDetails>
                                    <fopDetails>
                                        <fopCode>{form_of_payment_code}</fopCode>
                                    </fopDetails>
                                </fopPNRDetails>
                            </mopDetails>
                            <paymentModule>
                                <groupUsage>
                                    <attributeDetails>
                                        <attributeType>{group_usage_attribute_type}</attributeType>
                                    </attributeDetails>
                                </groupUsage>
                                <paymentData>
                                    <merchantInformation>
                                        <companyCode>{company_code}</companyCode>
                                    </merchantInformation>
                                </paymentData>
                                <mopInformation>
                                    <fopInformation>
                                        <formOfPayment>
                                        <type>{form_of_payment_type}</type>
                                        </formOfPayment>
                                    </fopInformation>
                                    <dummy/>
                                    {sub_parts.fop_form_of_payment(fop)}
                                </mopInformation>
                                <dummy/>
                            </paymentModule>
                            </mopDescription>
                        </fopGroup>
                    </FOP_CreateFormOfPayment>
                </soapenv:Body>
                </soapenv:Envelope>
                """
        else:

            return f"""
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                    xmlns:sec="http://xml.amadeus.com/2010/06/Security_v1"
                    xmlns:link="http://wsdl.amadeus.com/2010/06/ws/Link_v1"
                    xmlns:ses="http://xml.amadeus.com/2010/06/Session_v3"
                    xmlns:tfop="http://xml.amadeus.com/TFOPCQ_15_4_1A">
                {self.generate_header("PNRADD_17_1_1A", message_id, session_id, sequence_number, security_token, False)}
                <soapenv:Body>
                <PNR_AddMultiElements>
                    <pnrActions>
                        <optionCode>0</optionCode>
                    </pnrActions>
                    <dataElementsMaster>
                        <marker1/>
                        <dataElementsIndiv>
                            <elementManagementData>
                                <segmentName>FP</segmentName>
                            </elementManagementData>
=======
        vendor_code = fop.vendor_code
        carte_number = fop.card_number
        security_id = fop.security_id
        expiry_date = fop.expiry_date
        return f"""
           <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:sec="http://xml.amadeus.com/2010/06/Security_v1" xmlns:link="http://wsdl.amadeus.com/2010/06/ws/Link_v1" xmlns:ses="http://xml.amadeus.com/2010/06/Session_v3" xmlns:tfop="http://xml.amadeus.com/TFOPCQ_15_4_1A">
       <soapenv:Header xmlns:add="http://www.w3.org/2005/08/addressing">
       <add:MessageID>{message_id}</add:MessageID>
       <add:Action>http://webservices.amadeus.com/TFOPCQ_15_4_1A</add:Action>
       <add:To>{self.endpoint}/{self.wsap}</add:To>
       {security_part}
       </soapenv:Header>
       <soapenv:Body>
          <FOP_CreateFormOfPayment>
             <transactionContext>
                <transactionDetails>
                <code>{form_of_payment}</code>
                </transactionDetails>
             </transactionContext>
             <fopGroup>
                <fopReference></fopReference>
                <passengerAssociation>
                   <passengerReference>
                      <type>{passenger_reference_type}</type>
                      <value>{passenger_reference_value}</value>
                   </passengerReference>
                </passengerAssociation>
                <mopDescription>
                   <fopSequenceNumber>
                      <sequenceDetails>
                         <number>{form_of_payment_sequence_number}</number>
                      </sequenceDetails>
                   </fopSequenceNumber>
                   <mopDetails>
                      <fopPNRDetails>
                         <fopDetails>
                            <fopCode>{form_of_payment_code}</fopCode>
                         </fopDetails>
                      </fopPNRDetails>
                   </mopDetails>
                   <paymentModule>
                      <groupUsage>
                         <attributeDetails>
                            <attributeType>{group_usage_attribute_type}</attributeType>
                         </attributeDetails>
                      </groupUsage>
                      <paymentData>
                         <merchantInformation>
                            <companyCode>{company_code}</companyCode>
                         </merchantInformation>
                      </paymentData>
                      <mopInformation>
                         <fopInformation>
>>>>>>> 03ae67bb20447cd73e03eec553f9d9cb4c44a07a
                            <formOfPayment>
                                <fop>
                                    <identification>{form_of_payment_type}</identification>
                                </fop>
                            </formOfPayment>
<<<<<<< HEAD
                        </dataElementsIndiv>
                    </dataElementsMaster>
                </PNR_AddMultiElements>
                </soapenv:Body>
                </soapenv:Envelope>"""
=======
                         </fopInformation>
                         <dummy/>
                         <creditCardData>
                            <creditCardDetails>
                               <ccInfo>
                                  <vendorCode>{vendor_code}</vendorCode>
                                  <cardNumber>{carte_number}</cardNumber>
                                  <securityId>{security_id}</securityId>
                                  <expiryDate>{expiry_date}</expiryDate>
                               </ccInfo>
                            </creditCardDetails>
                         </creditCardData>
                      </mopInformation>
                      <dummy/>
                   </paymentModule>
                </mopDescription>
             </fopGroup>
          </FOP_CreateFormOfPayment>
       </soapenv:Body>
       </soapenv:Envelope>
    """
>>>>>>> 03ae67bb20447cd73e03eec553f9d9cb4c44a07a

    def ticket_pnr_builder(self, message_id, session_id, sequence_number, security_token, passenger_reference_type,
                           passenger_reference_value):
        return f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
        xmlns:sec="http://xml.amadeus.com/2010/06/Security_v1"
        xmlns:typ="http://xml.amadeus.com/2010/06/Types_v1"
        xmlns:iat="http://www.iata.org/IATA/2007/00/IATA2010.1"
        xmlns:app="http://xml.amadeus.com/2010/06/AppMdw_CommonTypes_v3"
        xmlns:link="http://wsdl.amadeus.com/2010/06/ws/Link_v1"
        xmlns:ses="http://xml.amadeus.com/2010/06/Session_v3">
            {self.generate_header("TTKTIQ_15_1_1A", message_id, session_id, sequence_number, security_token)}
            <soapenv:Body>
                <DocIssuance_IssueTicket>
                    <paxSelection>
                        <passengerReference>
                            <type>{passenger_reference_type}</type>
                            <value>{passenger_reference_value}</value>
                        </passengerReference>
                    </paxSelection>
                </DocIssuance_IssueTicket>
            </soapenv:Body>
        </soapenv:Envelope>
    """

<<<<<<< HEAD
    def pnr_add_multi_element_builder(self, session_id, sequence_number, security_token, message_id, option_code, segment_name):
        # security_part = self.continue_transaction_chunk(session_id, sequence_number, security_token)
        # <nameInformation>
        #     <qualifier>RF</qualifier>
        #     <name>KOKOU</name>
        # </nameInformation>
=======
    def pnr_add_multi_element_builder(self, session_id, sequence_number, security_token, message_id, option_code,
                                      segment_name, identification, credit_card_code, account_number, expiry_date,
                                      currency_code):
        security_part = self.continue_transaction_chunk(session_id, sequence_number, security_token)
>>>>>>> 03ae67bb20447cd73e03eec553f9d9cb4c44a07a
        return f"""
                <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:sec="http://xml.amadeus.com/2010/06/Security_v1" xmlns:typ="http://xml.amadeus.com/2010/06/Types_v1" xmlns:iat="http://www.iata.org/IATA/2007/00/IATA2010.1" xmlns:app="http://xml.amadeus.com/2010/06/AppMdw_CommonTypes_v3" xmlns:link="http://wsdl.amadeus.com/2010/06/ws/Link_v1" xmlns:ses="http://xml.amadeus.com/2010/06/Session_v3">
    <soapenv:Header xmlns:add="http://www.w3.org/2005/08/addressing">
    <add:MessageID>{message_id}</add:MessageID>
    <add:Action>http://webservices.amadeus.com/TTKTIQ_15_1_1A</add:Action>
    <add:To>{self.endpoint}/{self.wsap}</add:To>{security_part}
    </soapenv:Header>
    <soapenv:Body>
            <PNR_AddMultiElements>
      <pnrActions>
        <optionCode>{option_code}</optionCode>
      </pnrActions>
      <dataElementsMaster>
        <marker1 />
        <dataElementsIndiv>
          <elementManagementData>
            <segmentName>{segment_name}</segmentName>
          </elementManagementData>
          <formOfPayment>
            <fop>
              <identification>{identification}</identification>
              <creditCardCode>{credit_card_code}</creditCardCode>
              <accountNumber>{account_number}</accountNumber>
              <expiryDate>{expiry_date}</expiryDate>
              <currencyCode>{currency_code}</currencyCode>
            </fop>
            # <fop>
            #   <identification>CA</identification>
            #   <amount>96.46</amount>
            # </fop>
          </formOfPayment>
        </dataElementsIndiv>
      </dataElementsMaster>
    </PNR_AddMultiElements>
       </soapenv:Body>
    </soapenv:Envelope> """

    def pnr_add_multi_element_for_pax_info_builder(self, session_id, sequence_number, security_token, message_id, ref_number,
                                                   surname, quantity, first_name, pax_type, inf_number, date_of_birth):

        return f"""
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                xmlns:sec="http://xml.amadeus.com/2010/06/Security_v1"
                xmlns:typ="http://xml.amadeus.com/2010/06/Types_v1"
                xmlns:iat="http://www.iata.org/IATA/2007/00/IATA2010.1"
                xmlns:app="http://xml.amadeus.com/2010/06/AppMdw_CommonTypes_v3"
                xmlns:link="http://wsdl.amadeus.com/2010/06/ws/Link_v1"
                xmlns:ses="http://xml.amadeus.com/2010/06/Session_v3">
                {self.generate_header("PNRADD_17_1_1A", message_id, session_id, sequence_number, security_token)}
                <soapenv:Body>
                    <PNR_AddMultiElements>
                        <pnrActions>
                            <optionCode>0</optionCode>
                        </pnrActions>
                        <travellerInfo>
                            <elementManagementPassenger>
                                <reference>
                                    <qualifier>PT</qualifier>
                                    <number>{ref_number}</number>
                                </reference>
                                <segmentName>NM</segmentName>
                            </elementManagementPassenger>
                            <passengerData>
                                <travellerInformation>
                                    <traveller>
                                        <surname>{surname}</surname>
                                        <quantity>{quantity}</quantity>
                                    </traveller>
                                    <passenger>
                                        <firstName>{first_name}</firstName>
                                        <type>{pax_type}</type>
                                        <infantIndicator>{inf_number}</infantIndicator>
                                    </passenger>
                                </travellerInformation>
                                <dateOfBirth>
                                    <dateAndTimeDetails>
                                        <date>{date_of_birth}</date>
                                    </dateAndTimeDetails>
                                </dateOfBirth>
                            </passengerData>
                        </travellerInfo>
                    </PNR_AddMultiElements>
                </soapenv:Body>
            </soapenv:Envelope> """

    def issue_ticket_retrieve(self, message_id, security_token, sequence_number, session_id, tst_refs: List[str]):
        return f"""
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                xmlns:sec="http://xml.amadeus.com/2010/06/Security_v1"
                xmlns:typ="http://xml.amadeus.com/2010/06/Types_v1"
                xmlns:iat="http://www.iata.org/IATA/2007/00/IATA2010.1"
                xmlns:app="http://xml.amadeus.com/2010/06/AppMdw_CommonTypes_v3"
                xmlns:link="http://wsdl.amadeus.com/2010/06/ws/Link_v1"
                xmlns:ses="http://xml.amadeus.com/2010/06/Session_v3">
               {self.generate_header("TTKTIQ_15_1_1A", message_id, session_id, sequence_number, security_token, False)}
               <soapenv:Body>
                  <DocIssuance_IssueTicket>
                     <selection>
                        {"".join([sub_parts.ticket_issue_tst_ref(r) for r in tst_refs])}
                    </selection>
                  </DocIssuance_IssueTicket>
               </soapenv:Body>
            </soapenv:Envelope>
        """

    def queue_place_pnr(self, message_id: str, session_id: str, sequence_number: str, security_token: str, pnr: str, queues: List[str]):
        header = self.generate_header("QUQPCQ_03_1_1A", message_id, session_id, sequence_number, security_token)
        return f"""
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
            xmlns:sec="http://xml.amadeus.com/2010/06/Security_v1"
            xmlns:typ="http://xml.amadeus.com/2010/06/Types_v1"
            xmlns:iat="http://www.iata.org/IATA/2007/00/IATA2010.1"
            xmlns:app="http://xml.amadeus.com/2010/06/AppMdw_CommonTypes_v3"
            xmlns:link="http://wsdl.amadeus.com/2010/06/ws/Link_v1"
            xmlns:ses="http://xml.amadeus.com/2010/06/Session_v3">
            {header}
            <soapenv:Body>
                <Queue_PlacePNR>
                    <placementOption>
                        <selectionDetails>
                            <option>QEQ</option>
                        </selectionDetails>
                    </placementOption>
                    {"".join([sub_parts.queue_place_target_queue(self.office_id, q, "0") for q in queues])}
                    <recordLocator>
                        <reservation>
                            <controlNumber>{pnr}</controlNumber>
                        </reservation>
                    </recordLocator>
                </Queue_PlacePNR>
            </soapenv:Body>
        </soapenv:Envelope>"""

    def fare_informative_best_pricing_without_pnr(self, message_id, session_id, sequence_number, security_token, numbering: TravellerNumbering, itineraries: List[Itinerary]):

        return f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:sec="http://xml.amadeus.com/2010/06/Security_v1" xmlns:typ="http://xml.amadeus.com/2010/06/Types_v1" xmlns:iat="http://www.iata.org/IATA/2007/00/IATA2010.1" xmlns:app="http://xml.amadeus.com/2010/06/AppMdw_CommonTypes_v3" xmlns:link="http://wsdl.amadeus.com/2010/06/ws/Link_v1" xmlns:ses="http://xml.amadeus.com/2010/06/Session_v3">
           {self.generate_header("QUQPCQ_03_1_1A", message_id, session_id, sequence_number, security_token)}
           <soapenv:Body>
              <Fare_InformativePricingWithoutPNR>
                 {sub_parts.fare_informative_price_passengers(numbering)}
                 {sub_parts.fare_informative_price_segments(itineraries)}
              </Fare_InformativePricingWithoutPNR>
            </soapenv:Body>
        </soapenv:Envelope>
        """

    def issue_combined(self, session_info: SessionInfo, passengers: List[str],
                       segments: List[str], retrieve_pnr: bool = False):
        message_id = session_info.message_id
        session_id = session_info.session_id
        sequence_number = session_info.sequence_number
        security_token = session_info.security_token

        return f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
            xmlns:sec="http://xml.amadeus.com/2010/06/Security_v1"
            xmlns:typ="http://xml.amadeus.com/2010/06/Types_v1"
            xmlns:iat="http://www.iata.org/IATA/2007/00/IATA2010.1"
            xmlns:app="http://xml.amadeus.com/2010/06/AppMdw_CommonTypes_v3"
            xmlns:link="http://wsdl.amadeus.com/2010/06/ws/Link_v1"
            xmlns:ses="http://xml.amadeus.com/2010/06/Session_v3">
            {self.generate_header("TCTMIQ_15_1_1A", message_id, session_id, sequence_number, security_token)}
            <soapenv:Body>
                <DocIssuance_IssueCombined xmlns="http://xml.amadeus.com/TCTMIQ_15_1_1A">
                    {sub_parts.itc_segment_select(segments) if segments else ""}
                    {"".join([sub_parts.itc_pax_selection(p) for p in passengers])}
                    {sub_parts.itc_option_group("TKT")}
                    {sub_parts.itc_option_group("RT") if retrieve_pnr else ""}
                </DocIssuance_IssueCombined>
            </soapenv:Body>
        </soapenv:Envelope>
        """

    def void_tickets(self, session_info: SessionInfo, ticket_numbers: List[str]):
        message_id = session_info.message_id
        session_id = session_info.session_id
        sequence_number = session_info.sequence_number
        security_token = session_info.security_token
        return f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
            xmlns:sec="http://xml.amadeus.com/2010/06/Security_v1"
            xmlns:typ="http://xml.amadeus.com/2010/06/Types_v1"
            xmlns:iat="http://www.iata.org/IATA/2007/00/IATA2010.1"
            xmlns:app="http://xml.amadeus.com/2010/06/AppMdw_CommonTypes_v3"
            xmlns:link="http://wsdl.amadeus.com/2010/06/ws/Link_v1"
            xmlns:ses="http://xml.amadeus.com/2010/06/Session_v3">
            {self.generate_header("TRCANQ_11_1_1A", message_id, session_id, sequence_number, security_token)}
            <soapenv:Body>
                <Ticket_CancelDocument xmlns="http://xml.amadeus.com/TRCANQ_11_1_1A" >
                    {"".join([sub_parts.tcd_ticket_number(t) for t in ticket_numbers])}
                    <stockProviderDetails>
                        <officeSettingsDetails>
                            <stockProviderCode>6X</stockProviderCode>
                        </officeSettingsDetails>
                    </stockProviderDetails>
                </Ticket_CancelDocument>
            </soapenv:Body>
        </soapenv:Envelope>
        """

    def cancel_pnr(self, session_info: SessionInfo, close_session: bool = False):
        message_id = session_info.message_id
        session_id = session_info.session_id
        sequence_number = session_info.sequence_number
        security_token = session_info.security_token
        return f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
            {self.generate_header("PNRXCL_17_1_1A", message_id, session_id, sequence_number, security_token, close_session)}
            <soapenv:Body>
                <PNR_Cancel xmlns="http://xml.amadeus.com/PNRXCL_17_1_1A">
                    <pnrActions>
                        <optionCode>10</optionCode>
                    </pnrActions>
                    <cancelElements>
                        <entryType>I</entryType>
                    </cancelElements>
                </PNR_Cancel>
            </soapenv:Body>
        </soapenv:Envelope>
        """
