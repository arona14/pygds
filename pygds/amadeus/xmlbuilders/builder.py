from time import gmtime, strftime
from typing import List
from pygds.amadeus.xmlbuilders import sub_parts
from pygds.amadeus.xmlbuilders import low_fare_search_helper
from pygds.core.sessions import SessionInfo
from pygds.core.types import TravellerNumbering, Itinerary, Recommandation
from pygds.core.request import LowFareSearchRequest
from pygds.core.payment import ChashPayment
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

    def cancel_segments(self, session_id, sequence_number, security_token, message_id, segments):

        return f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:sec="http://xml.amadeus.com/2010/06/Security_v1" xmlns:typ="http://xml.amadeus.com/2010/06/Types_v1" xmlns:iat="http://www.iata.org/IATA/2007/00/IATA2010.1" xmlns:app="http://xml.amadeus.com/2010/06/AppMdw_CommonTypes_v3" xmlns:link="http://wsdl.amadeus.com/2010/06/ws/Link_v1" xmlns:ses="http://xml.amadeus.com/2010/06/Session_v3">
             {self.generate_header("PNRXCL_14_2_1A", message_id, session_id, sequence_number, security_token)}
            <soapenv:Body>
                <PNR_Cancel>
                    <pnrActions>
                        <optionCode>11</optionCode>
                    </pnrActions>
                    <cancelElements>
                        <entryType>E</entryType>
                        {''.join([f'''<element>
                                    <identifier>SS</identifier>
                                    <number>{segment}</number>
                                </element>''' for segment in segments
                        ])}
                    </cancelElements>
                </PNR_Cancel>
            </soapenv:Body>
        </soapenv:Envelope>
        """

    def cancel_information_passenger(self, session_id, sequence_number, security_token,
                                     message_id, reference):
        return f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:sec="http://xml.amadeus.com/2010/06/Security_v1" xmlns:typ="http://xml.amadeus.com/2010/06/Types_v1" xmlns:iat="http://www.iata.org/IATA/2007/00/IATA2010.1" xmlns:app="http://xml.amadeus.com/2010/06/AppMdw_CommonTypes_v3" xmlns:link="http://wsdl.amadeus.com/2010/06/ws/Link_v1" xmlns:ses="http://xml.amadeus.com/2010/06/Session_v3">
             {self.generate_header("PNRXCL_14_2_1A", message_id, session_id, sequence_number, security_token)}
            <soapenv:Body>
                <PNR_Cancel>
                    <pnrActions>
                        <optionCode>11</optionCode>
                    </pnrActions>
                    <cancelElements>
                        <entryType>E</entryType>
                        <element>
                        <identifier>OT</identifier>
                        <number>{reference}</number>
                        </element>
                    </cancelElements>
                </PNR_Cancel>
            </soapenv:Body>
        </soapenv:Envelope>
        """

    def get_reservation_builder(self, message_id: str = None, session_id: str = None,
                                sequence_number: str = None, security_token: str = None, pnr_number: str = None, close_trx: bool = False):
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

    def fare_master_pricer_travel_board_search(self, office_id, low_fare_search: LowFareSearchRequest):
        """
            Search prices for origin/destination and departure/arrival dates
        """

        message_id, nonce, created_date_time, digested_password = self.ensure_security_parameters(None, None, None)
        security_part = self.new_transaction_chunk(self.office_id, self.username, nonce, digested_password,
                                                   created_date_time, True)
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
                            {low_fare_search_helper.generate_number_of_unit(low_fare_search.travelingNumber, low_fare_search.number_of_unit_rc)}
                            {low_fare_search_helper.generate_pax_reference(low_fare_search.travelingNumber)}
                            {low_fare_search_helper.generate_fare_options(low_fare_search.fare_options)}
                            {low_fare_search_helper.generate_travel_flight_info(low_fare_search.travel_flight_info)}
                            {low_fare_search_helper.generate_itinerary(low_fare_search.itineraries)}
                        </Fare_MasterPricerTravelBoardSearch>
                    </soapenv:Body>
                </soapenv:Envelope>
                """

    def fare_informative_price_without_pnr(self, numbering: TravellerNumbering, itineraries: List[Itinerary]):

        message_id, nonce, created_date_time, digested_password = self.ensure_security_parameters(None, None, None)
        security_part = self.new_transaction_chunk(self.office_id, self.username, nonce, digested_password,
                                                   created_date_time, True)

        header = f"""<soapenv:Header xmlns:add="http://www.w3.org/2005/08/addressing">
                        <add:MessageID>{message_id}</add:MessageID>
                        <add:Action>http://webservices.amadeus.com/TIBNRQ_18_1_1A</add:Action>
                        <add:To>{self.endpoint}/{self.wsap}</add:To>
                        {security_part}
                    </soapenv:Header>"""

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

    def fare_informative_best_price_without_pnr(self, recommandation: Recommandation):
        message_id, nonce, created_date_time, digested_password = self.ensure_security_parameters(None, None, None)
        security_part = self.new_transaction_chunk(self.office_id, self.username, nonce, digested_password,
                                                   created_date_time, True)
        header = f"""<soapenv:Header xmlns:add="http://www.w3.org/2005/08/addressing">
                        <add:MessageID>{message_id}</add:MessageID>
                        <add:Action>http://webservices.amadeus.com/TIBNRQ_18_1_1A</add:Action>
                        <add:To>{self.endpoint}/{self.wsap}</add:To>
                        {security_part}
                    </soapenv:Header>"""

        pricing_options_group = ""

        if recommandation.fare_options.price_type_rp:
            pricing_options_group += f"""<pricingOptionGroup>
                                            <pricingOptionKey>
                                                <pricingOptionKey>RP</pricingOptionKey>
                                            </pricingOptionKey>
                                        </pricingOptionGroup>"""

        if recommandation.fare_options.price_type_ru:
            pricing_options_group += f"""<pricingOptionGroup>
                                            <pricingOptionKey>
                                                <pricingOptionKey>RU</pricingOptionKey>
                                            </pricingOptionKey>
                                        </pricingOptionGroup>"""
        return f"""
                <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:sec="http://xml.amadeus.com/2010/06/Security_v1" xmlns:typ="http://xml.amadeus.com/2010/06/Types_v1" xmlns:iat="http://www.iata.org/IATA/2007/00/IATA2010.1" xmlns:app="http://xml.amadeus.com/2010/06/AppMdw_CommonTypes_v3" xmlns:link="http://wsdl.amadeus.com/2010/06/ws/Link_v1" xmlns:ses="http://xml.amadeus.com/2010/06/Session_v3">
                    {header}
                    <soapenv:Body>
                        <Fare_InformativeBestPricingWithoutPNR>
                            {sub_parts.fare_informative_best_price_passengers(recommandation.traveller_numbering)}
                            {sub_parts.fare_informative_best_price_segment(recommandation.segments)}
                            {pricing_options_group}
                        </Fare_InformativeBestPricingWithoutPNR>
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
                                          fare_type: str = "",
                                          passengers: list = [],
                                          segments: list = []):
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
                    {sub_parts.ppwbc_fare_type(fare_type)}
                    {sub_parts.ppwbc_passenger_segment_selection(passengers, segments)}
                </Fare_PricePNRWithBookingClass>
            </soapenv:Body>
        </soapenv:Envelope>
        """

    def ticket_create_tst_from_price(self, message_id, session_id, sequence_number, security_token, tst_references: List[str] = []):
        security_part = self.continue_transaction_chunk(session_id, sequence_number, security_token)

        content = ""
        for tst_ref in tst_references:
            content += f"""<psaList>
                                <itemReference>
                                <referenceType>TST</referenceType>
                                <uniqueReference>{tst_ref}</uniqueReference>
                                </itemReference>
                            </psaList>"""

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
                            {content}
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

    def get_fare_rules(self, ticketing_date, rate_class, company_id, origin, destination):

        message_id, nonce, created_date_time, digested_password = self.ensure_security_parameters(None, None, None)
        security_part = self.new_transaction_chunk(self.office_id, self.username, nonce, digested_password,
                                                   created_date_time, True)
        header = f"""<soapenv:Header xmlns:add="http://www.w3.org/2005/08/addressing">
                        <add:MessageID>{message_id}</add:MessageID>
                        <add:Action>http://webservices.amadeus.com/FARRNQ_10_1_1A</add:Action>
                        <add:To>{self.endpoint}/{self.wsap}</add:To>
                        {security_part}
                    </soapenv:Header>"""

        return f"""
                <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:sec="http://xml.amadeus.com/2010/06/Security_v1" xmlns:typ="http://xml.amadeus.com/2010/06/Types_v1" xmlns:iat="http://www.iata.org/IATA/2007/00/IATA2010.1" xmlns:app="http://xml.amadeus.com/2010/06/AppMdw_CommonTypes_v3" xmlns:link="http://wsdl.amadeus.com/2010/06/ws/Link_v1" xmlns:ses="http://xml.amadeus.com/2010/06/Session_v3">
                    {header}
                    <soapenv:Body>
                    <Fare_GetFareRules>
                        <msgType>
                            <messageFunctionDetails>
                                <messageFunction>FRN</messageFunction>
                            </messageFunctionDetails>
                        </msgType>
                        <pricingTickInfo>
                            <productDateTimeDetails>
                                <ticketingDate>{ticketing_date}</ticketingDate>
                            </productDateTimeDetails>
                        </pricingTickInfo>
                        <flightQualification>
                            <additionalFareDetails>
                                <rateClass>{rate_class}</rateClass>
                            </additionalFareDetails>
                        </flightQualification>
                        <transportInformation>
                            <transportService>
                                <companyIdentification>
                                    <marketingCompany>{company_id}</marketingCompany>
                                </companyIdentification>
                            </transportService>
                        </transportInformation>
                        <tripDescription>
                            <origDest>
                                <origin>{origin}</origin>
                                <destination>{destination}</destination>
                            </origDest>
                        </tripDescription>
                    </Fare_GetFareRules>
                </soapenv:Body>
            </soapenv:Envelope> """

    def sell_from_recomendation(self, itineraries):

        message_id, nonce, created_date_time, digested_password = self.ensure_security_parameters(None, None, None)
        security_part = self.new_transaction_chunk(self.office_id, self.username, nonce, digested_password,
                                                   created_date_time)
        itineraries_details = []
        for itinerary in itineraries:
            # itineraries_details.append(sub_parts.sell_from_recommendation_itinerary_details(it.origin, it.destination, it.segments))
            itineraries_details.append(
                self.itenerary_details(itinerary.origin, itinerary.destination, itinerary))
        # The optimization algorithm. M1: cancel all if unsuccessful, M2: keep all confirmed if unsuccessful
        algo = 'M1'

        header = f"""<soapenv:Header xmlns:add="http://www.w3.org/2005/08/addressing">
                        <add:MessageID>{message_id}</add:MessageID>
                        <add:Action>http://webservices.amadeus.com/ITAREQ_05_2_IA</add:Action>
                        <add:To>{self.endpoint}/{self.wsap}</add:To>
                        {security_part}
                    </soapenv:Header>"""

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

    def itenerary_details(self, origin, destination, itinerary):

        seg_infos = ""

        for segment in itinerary.segments:
            seg_infos += f"""
                        <segmentInformation>
                            <travelProductInformation>
                                <flightDate>
                                    <departureDate>{segment.departure_date}</departureDate>
                                </flightDate>
                                <boardPointDetails>
                                    <trueLocationId>{segment.origin}</trueLocationId>
                                </boardPointDetails>
                                <offpointDetails>
                                    <trueLocationId>{segment.destination}</trueLocationId>
                                </offpointDetails>
                                <companyDetails>
                                    <marketingCompany>{segment.company}</marketingCompany>
                                </companyDetails>
                                <flightIdentification>
                                    <flightNumber>{segment.flight_number}</flightNumber>
                                    <bookingClass>{segment.booking_class}</bookingClass>
                                </flightIdentification>
                            </travelProductInformation>
                            <relatedproductInformation>
                                <quantity>{segment.quantity}</quantity>
                                <statusCode>NN</statusCode>
                            </relatedproductInformation>
                        </segmentInformation>"""
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
            {seg_infos}
        </itineraryDetails>
        """

    def add_passenger_info(self, office_id, message_id, session_id, sequence_number, security_token, infos):
        security_part = self.continue_transaction_chunk(session_id, sequence_number, security_token)
        passenger_infos = []
        ssr_content = ""
        email_tel_passengers = ""

        for i in infos.traveller_info:

            passenger_infos.append(
                sub_parts.add_multi_elements_traveller_info(
                    i.ref_number, i.first_name, i.surname, i.last_name, i.date_of_birth, i.pax_type, i.infant
                )
            )

            if i.pax_type == "ADT":
                ssr_content += sub_parts.add_multi_element_ssr(i)

            email_tel_passengers += sub_parts.add_multi_element_contact_element(
                "7", i.tel, i.ref_number
            ) if i.tel else ""

            email_tel_passengers += sub_parts.add_multi_element_contact_element(
                "P02", i.email, i.ref_number
            ) if i.email else ""

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
                        {email_tel_passengers}
                        {sub_parts.add_multi_element_contact_element("6", infos.number_tel_agent) if infos.number_tel else ""}
                        {ssr_content}
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

    def add_office_id(self, office_id, message_id, session_id, sequence_number, security_token):
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
                        <optionCode>0</optionCode>
                    </pnrActions>
                    <dataElementsMaster>
                        <marker1/>
                        {sub_parts.add_multi_element_data_element("RF", 3, "P22", office_id)}
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

    def add_form_of_payment_builder(self, message_id, session_id, sequence_number,
                                    security_token, fop, segment_refs, pax_refs, inf_refs, fop_sequence_number):

        form_of_payment = "DEF"  # "DEF
        pax_refs = pax_refs or []
        inf_refs = inf_refs or []
        segment_refs = segment_refs or []
        content = ""
        if not isinstance(fop, ChashPayment):
            form_of_payment_code = fop.p_code
            company_code = fop.company_code
            form_of_payment_type = fop.p_type
            group_usage_attribute_type = "FP"  # "PAY"

            content = sub_parts.fop_credit_card_and_check(
                form_of_payment_code, group_usage_attribute_type, company_code, form_of_payment_type, fop
            )

        else:
            content = f"""<mopDetails>
                            <fopPNRDetails>
                                <fopDetails>
                                    <fopCode>CASH</fopCode>
                                </fopDetails>
                            </fopPNRDetails>
                        </mopDetails>"""
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
                        <fopReference/>
                        {"".join([sub_parts.fop_passenger("PAX", ref) for ref in pax_refs])}
                        {"".join([sub_parts.fop_passenger("INF", ref) for ref in inf_refs])}
                        {"".join([sub_parts.fop_segment(ref) for ref in segment_refs])}
                        <mopDescription>
                        {sub_parts.fop_sequence_number(fop_sequence_number) if fop_sequence_number else "1"}
                        {content}
                        </mopDescription>
                    </fopGroup>
                </FOP_CreateFormOfPayment>
            </soapenv:Body>
            </soapenv:Envelope>
            """

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

    def pnr_add_multi_element_builder(self, session_id, sequence_number, security_token, message_id, option_code, segment_name):
        security_part = self.continue_transaction_chunk(session_id, sequence_number, security_token)
        # <nameInformation>
        #     <qualifier>RF</qualifier>
        #     <name>KOKOU</name>
        # </nameInformation>
        return f"""
                <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:sec="http://xml.amadeus.com/2010/06/Security_v1" xmlns:typ="http://xml.amadeus.com/2010/06/Types_v1" xmlns:iat="http://www.iata.org/IATA/2007/00/IATA2010.1" xmlns:app="http://xml.amadeus.com/2010/06/AppMdw_CommonTypes_v3" xmlns:link="http://wsdl.amadeus.com/2010/06/ws/Link_v1" xmlns:ses="http://xml.amadeus.com/2010/06/Session_v3">
    <soapenv:Header xmlns:add="http://www.w3.org/2005/08/addressing">
    <add:MessageID>{message_id}</add:MessageID>
    <add:Action>http://webservices.amadeus.com/PNRADD_17_1_1A</add:Action>
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
                                <segmentName>AIR</segmentName>
                            </elementManagementData>
                        </dataElementsIndiv>
                        <dataElementsIndiv>
                            <elementManagementData>
                                <segmentName>RF</segmentName>
                            </elementManagementData>
                                <freetextData>
                                    <freetextDetail>
                                        <subjectQualifier>3</subjectQualifier>
                                        <type>P22</type>
                                    </freetextDetail>
                                    <longFreetext>DTW1S210B</longFreetext>
                                </freetextData>
                            </dataElementsIndiv>
                    </dataElementsMaster>
    </PNR_AddMultiElements>
       </soapenv:Body>
    </soapenv:Envelope> """

    def pnr_add_multi_element_for_pax_info_builder(self, session_id, sequence_number, security_token, message_id, email_content, passenger_id, office_id):
        passenger_informations = sub_parts.build_update_principal_passenger(email_content, passenger_id, office_id)
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
                            <optionCode>11</optionCode>
                        </pnrActions>
                        {passenger_informations}
                    </PNR_AddMultiElements>
                </soapenv:Body>
            </soapenv:Envelope> """

    def pnr_add_ssr(self, session_id, sequence_number, security_token, message_id, passenger_ids, content, company_id):

        ssr_request = ""
        for id in passenger_ids:
            ssr_request += f"""<dataElementsIndiv>
                               <elementManagementData>
                                    <segmentName>SSR</segmentName>
                                </elementManagementData>
                                <serviceRequest>
                                   <ssr>
                                        <type>DOCS</type>
                                        <status>HK</status>
                                        <quantity>1</quantity>
                                        <companyId>{company_id}</companyId>
                                        <freetext>{content}</freetext>
                                    </ssr>
                                </serviceRequest>
                                <referenceForDataElement>
                                   <reference>
                                        <qualifier>PT</qualifier>
                                        <number>{id}</number>
                                    </reference>
                                </referenceForDataElement>
</dataElementsIndiv>"""
        return f"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
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
                <optionCode>11</optionCode>
                </pnrActions>
                <dataElementsMaster>
                <marker1/>
                {ssr_request}
                </dataElementsMaster>
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

    def create_tsm(self, session_info, passenger_id, tsm_type):
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
            {self.generate_header("TMCOCQ_07_3_1A", message_id, session_id, sequence_number, security_token)}
            <soapenv:Body>
                <PNR_CreateTSM>
                        <msg>
                            <messageFunctionDetails>
                                <businessFunction>47</businessFunction>
                            </messageFunctionDetails>
                        </msg>
                        <mcoData>
                            <paxTattoo>
                                <otherPaxDetails>
                                    <type>A</type>
                                    <uniqueCustomerIdentifier>{passenger_id}</uniqueCustomerIdentifier>
                                </otherPaxDetails>
                            </paxTattoo>
                            <totalFare>
                                <monetaryDetails>
                                    <typeQualifier>B</typeQualifier>
                                        <amount>10.00</amount>
                                    <currency>USD</currency>
                                </monetaryDetails>
                            </totalFare>
                            <genInfo>
                                <productDateTimeDetails>
                                    <departureDate>09AUG</departureDate>
                                </productDateTimeDetails>
                            </genInfo>
                            <freeTextInfo>
                                <freeTextQualification>
                                    <textSubjectQualifier>4</textSubjectQualifier>
                                    <informationType>47</informationType>
                                </freeTextQualification>
                                <freeText>NOCODE</freeText>
                                <freeText>RFI DESCRIPTION</freeText>
                            </freeTextInfo>
                            <mcoDocData>
                                <tktNumber>
                                    <documentDetails>
                                        <type>{tsm_type}</type>
                                    </documentDetails>
                                </tktNumber>
                            </mcoDocData>
                        </mcoData>
                </PNR_CreateTSM>
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
                            <marketIataCode>US</marketIataCode>
                        </officeSettingsDetails>
                    </stockProviderDetails>
                    <targetOfficeDetails>
                        <originatorDetails>
                            <inHouseIdentification2>{self.office_id}</inHouseIdentification2>
                        </originatorDetails>
                    </targetOfficeDetails>

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
