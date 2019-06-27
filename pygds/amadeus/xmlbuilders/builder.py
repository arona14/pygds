from time import gmtime, strftime

class AmadeusXMLBuilder():
    """
    This class is for generating the needed XML for SOAP requests
    """
    def __init__(self):
        self.current_timestamp = str(strftime("%Y-%m-%dT%H:%M:%S", gmtime()))

    def getReservationRQ(self, pcc, conversation_id, token, record_locator, status_session):
        return f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:sec="http://xml.amadeus.com/2010/06/Security_v1" xmlns:typ="http://xml.amadeus.com/2010/06/Types_v1" xmlns:iat="http://www.iata.org/IATA/2007/00/IATA2010.1" xmlns:app="http://xml.amadeus.com/2010/06/AppMdw_CommonTypes_v3" xmlns:link="http://wsdl.amadeus.com/2010/06/ws/Link_v1" xmlns:ses="http://xml.amadeus.com/2010/06/Session_v3">
   <soapenv:Header xmlns:add="http://www.w3.org/2005/08/addressing">
	<add:MessageID>{conversation_id}</add:MessageID>
	<add:Action>${=request.operation.action}</add:Action>
	<add:To>${#Endpoint}/${#Project#WSAP}</add:To>
	<oas:Security xmlns:oas="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" xmlns:oas1="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">
		<oas:UsernameToken oas1:Id="UsernameToken-1">
			<oas:Username>${#Project#UserId}</oas:Username>
			<oas:Nonce EncodingType="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-soap-message-security-1.0#Base64Binary">${#TestCase#Nonce}</oas:Nonce>
			<oas:Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordDigest">${#TestCase#Password}</oas:Password>
			<oas1:Created>${#TestCase#Created}</oas1:Created>
		</oas:UsernameToken>
	</oas:Security>
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
       # raise NotImplementedError("This method is not yet implemented")