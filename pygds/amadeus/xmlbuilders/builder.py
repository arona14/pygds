from time import gmtime, strftime
from security_utils import generate_random_message_id, generate_created, generate_nonce, password_digest


class AmadeusXMLBuilder():
    """
    This class is for generating the needed XML for SOAP requests
    """

    def __init__(self, endpoint, username, passord, office_id):
        self.current_timestamp = str(strftime("%Y-%m-%dT%H:%M:%S", gmtime()))
        self.endpoint = endpoint
        self.username = username,
        self.password_digest = password_digest(passord)
        self.office_id = office_id
        self.created_date_time = generate_created()

    def new_transaction_chunk(self, username, nonce, password_digested, created_date_time):
        return f"""
        <oas:Security xmlns:oas="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" xmlns:oas1="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">
            <oas:UsernameToken oas1:Id="UsernameToken-1">
                <oas:Username>{username}</oas:Username>
                <oas:Nonce EncodingType="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-soap-message-security-1.0#Base64Binary">{nonce}</oas:Nonce>
                <oas:Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordDigest">{password_digested}</oas:Password>
                <oas1:Created>{created_date_time}</oas1:Created>
            </oas:UsernameToken>
        </oas:Security>
       """

    def continue_transaction_chunk(self, session_id, sequence_number, security_token):
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
        if created_date_time is None:
            created_date_time = generate_created()

        if message_id is None:
            message_id = generate_random_message_id("TRX")

        if nonce is None:
            nonce = generate_nonce()
        digested_password = password_digest(password, nonce, created_date_time)

        return
        f"""
        <soapenv:Header xmlns:add="http://www.w3.org/2005/08/addressing">
            <add:MessageID>{message_id}</add:MessageID>
            <add:Action>http://webservices.amadeus.com/VLSSOQ_04_1_1A</add:Action>
            <add:To>{self.endpoint}/1ASIWCTSCSO</add:To>
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
            <awsse:Session TransactionStatusCode="Start" xmlns:awsse="http://xml.amadeus.com/2010/06/Session_v3"/>
        </soapenv:Header>
        """

    def getReservationRQ(self, pcc, conversation_id, token, record_locator, new_session=True):
        """
        Create XML request body for SOAP Operation getReservation. We use a given endpoint
        """
        if conversation_id is None:
            conversation_id = generate_random_message_id("GETRES")
        if new_session:
            status_session = "Start"
            security_part = self.new_transaction_chunk(self.username, self.nonce, self.password_digest)
        else:
            status_session = "InSeries"
            security_part = self.continue_transaction_chunk("", "", token)
        return f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:sec="http://xml.amadeus.com/2010/06/Security_v1" xmlns:typ="http://xml.amadeus.com/2010/06/Types_v1" xmlns:iat="http://www.iata.org/IATA/2007/00/IATA2010.1" xmlns:app="http://xml.amadeus.com/2010/06/AppMdw_CommonTypes_v3" xmlns:link="http://wsdl.amadeus.com/2010/06/ws/Link_v1" xmlns:ses="http://xml.amadeus.com/2010/06/Session_v3">
            <soapenv:Header xmlns:add="http://www.w3.org/2005/08/addressing">
            <add:MessageID>{conversation_id}</add:MessageID>
            <add:Action>http://webservices.amadeus.com/PNRRET_17_1_1A</add:Action>
            <add:To>${AmadeusXMLBuilder.endpoint}/1ASIWCTSCSO</add:To>
                {security_part}
            <AMA_SecurityHostedUser xmlns="http://xml.amadeus.com/2010/06/Security_v1">
                <UserID AgentDutyCode="SU" RequestorType="U" PseudoCityCode="{pcc}" POS_Type="1"/>
            </AMA_SecurityHostedUser>
            <awsse:Session TransactionStatusCode="{status_session}" xmlns:awsse="http://xml.amadeus.com/2010/06/Session_v3"/>
            </soapenv:Header>
            <soapenv:Body>
                <PNR_Retrieve>
                    <retrievalFacts>
                        <retrieve>
                        <type>2</type>
                        </retrieve>
                        <reservationOrProfileIdentifier>
                        <reservation>
                            <controlNumber>{record_locator}</controlNumber>
                        </reservation>
                        </reservationOrProfileIdentifier>
                    </retrievalFacts>
                </PNR_Retrieve>
            </soapenv:Body>
        </soapenv:Envelope>
        """
