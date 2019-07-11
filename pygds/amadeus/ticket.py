import requests
from .xmlbuilders.builder import AmadeusXMLBuilder
from ..env_settings import get_setting


class AmadeusTicketing:
    """This class allows the process of ticketing by using a set of functions such as add_form_of_payment()
    : this adds to the pnr forms of payment for each passenger. It takes into parameter the pnr,
    : the form of payment (cash, credit card, check and transfer), id of the passenger ...
    : the function ticketing() manages the ticketing part taking into account the passenger's id and its type"""

    def add_form_of_payment(self, message_id, session_id, sequence_number, security_token, form_of_payment, passenger_reference_type, passenger_reference_value, form_of_payment_sequence_number, form_of_payment_code, group_usage_attribute_type, company_code, form_of_payment_type, vendor_code, carte_number, security_id, expiry_date):
        try:
            url = "https://nodeD1.test.webservices.amadeus.com"
            header = {'Content-Type': 'text/xml;charset=UTF-8', 'Accept-Encoding': 'gzip,deflate', 'SOAPAction': 'http://webservices.amadeus.com/TFOPCQ_15_4_1A'}
            endpoint = get_setting("AMADEUS_ENDPOINT_URL")
            username = get_setting("AMADEUS_USERNAME")
            password = get_setting("AMADEUS_PASSWORD")
            office_id = "DTW1S210B"
            wsap = get_setting("AMADEUS_WSAP")
            add_fop = AmadeusXMLBuilder(endpoint, username, password, office_id, wsap).add_form_of_payment(message_id, session_id, sequence_number, security_token, form_of_payment, passenger_reference_type, passenger_reference_value, form_of_payment_sequence_number, form_of_payment_code, group_usage_attribute_type, company_code, form_of_payment_type, vendor_code, carte_number, security_id, expiry_date)
            response = requests.post(url, data=add_fop, headers=header)
            print(response.content)
            status_code = response.status_code
        except Exception as e:
            print(e)
            # TODO: Capture the real exception not the general one
            raise e
        return status_code

    def tiketing(self, message_id, session_id, sequence_number, security_token, passenger_reference_type, passenger_reference_value):
        try:
            url = "https://nodeD1.test.webservices.amadeus.com"
            header = {'Content-Type': 'text/xml;charset=UTF-8', 'Accept-Encoding': 'gzip,deflate', 'SOAPAction': 'http://webservices.amadeus.com/TTKTIQ_15_1_1A'}
            endpoint = get_setting("AMADEUS_ENDPOINT_URL")
            username = get_setting("AMADEUS_USERNAME")
            password = get_setting("AMADEUS_PASSWORD")
            office_id = "DTW1S210B"
            wsap = get_setting("AMADEUS_WSAP")
            ticket_res = AmadeusXMLBuilder(endpoint, username, password, office_id, wsap).add_ticket_pnr(message_id, session_id, sequence_number, security_token, passenger_reference_type, passenger_reference_value)
            response = requests.post(url, data=ticket_res, headers=header)
            print(response.status_code)
            status_code = response.content
        except Exception as e:
            print(e)
            raise e
        return status_code


def test():
    message_id = "S32B6N"
    session_id = "001M3SSTV1"
    security_token = "2I2R99GX9MUSP7UNGQ7EIZYJ6"
    vendor_code = "CA"
    carte_number = "5100290029002909"
    security_id = "737"
    expiry_date = "1020"
    form_of_payment = "FP"
    passenger_reference_type = "PT"
    passenger_reference_value = "3"
    form_of_payment_sequence_number = "1"
    form_of_payment_code = "CCVI"
    group_usage_attribute_type = "FP"
    company_code = "LO"
    form_of_payment_type = "CC"
    sequence_number = "1"
    print(AmadeusTicketing().add_form_of_payment(message_id, session_id, sequence_number, security_token, form_of_payment, passenger_reference_type, passenger_reference_value, form_of_payment_sequence_number, form_of_payment_code, group_usage_attribute_type, company_code, form_of_payment_type, vendor_code, carte_number, security_id, expiry_date))
    print(AmadeusTicketing().tiketing(message_id, session_id, sequence_number, security_token, passenger_reference_type, passenger_reference_value))


if __name__ == "__main__":
    test()


def tester():
    url = "https://nodeD1.test.webservices.amadeus.com"
    header = {'Content-Type': 'text/xml;charset=UTF-8', 'Accept-Encoding': 'gzip,deflate', 'SOAPAction': 'http://webservices.amadeus.com/PNRADD_17_1_1A'}
    data_ = f"""
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:sec="http://xml.amadeus.com/2010/06/Security_v1" xmlns:typ="http://xml.amadeus.com/2010/06/Types_v1" xmlns:iat="http://www.iata.org/IATA/2007/00/IATA2010.1" xmlns:app="http://xml.amadeus.com/2010/06/AppMdw_CommonTypes_v3" xmlns:link="http://wsdl.amadeus.com/2010/06/ws/Link_v1" xmlns:ses="http://xml.amadeus.com/2010/06/Session_v3">
   <soapenv:Header xmlns:add="http://www.w3.org/2005/08/addressing">
<add:MessageID>WbsConsu-qz237F9j1KUhvBhBQH12jJ6E5bCfIrB-RzIWG9Egc</add:MessageID>
<add:Action>http://webservices.amadeus.com/PNRADD_17_1_1A</add:Action>
<add:To>https://nodeD1.test.webservices.amadeus.com/1ASIWCTSCSO</add:To>
<awsse:Session TransactionStatusCode="InSeries" xmlns:awsse="http://xml.amadeus.com/2010/06/Session_v3">
<awsse:SessionId>01EJ9C3WFR</awsse:SessionId>
<awsse:SequenceNumber>2</awsse:SequenceNumber>
<awsse:SecurityToken>30VLLG44XVNY419E1CR1DEU5QL</awsse:SecurityToken>
</awsse:Session>
</soapenv:Header>
<soapenv:Body>
<PNR_AddMultiElements>
         <pnrActions>
            <optionCode>0</optionCode>
         </pnrActions>
         <travellerInfo>
            <elementManagementPassenger>
               <reference>
                  <qualifier>PR</qualifier>
                  <number>1</number>
               </reference>
               <segmentName>NM</segmentName>
            </elementManagementPassenger>
            <passengerData>
               <travellerInformation>
                  <traveller>
                     <surname>Bolanos</surname>
                     <quantity>1</quantity>
                  </traveller>
                  <passenger>
                     <firstName>Germain</firstName>
                     <type>ADT</type>
                  </passenger>
               </travellerInformation>
               <dateOfBirth>
                  <dateAndTimeDetails>
                     <date>10JUN78</date>
                  </dateAndTimeDetails>
               </dateOfBirth>
            </passengerData>
         </travellerInfo>
         <travellerInfo>
            <elementManagementPassenger>
               <reference>
                  <qualifier>PR</qualifier>
                  <number>2</number>
               </reference>
               <segmentName>NM</segmentName>
            </elementManagementPassenger>
            <passengerData>
               <travellerInformation>
                  <traveller>
                     <surname>Alex</surname>
                     <quantity>1</quantity>
                  </traveller>
                  <passenger>
                     <firstName>Andra</firstName>
                     <type>ADT</type>
                  </passenger>
               </travellerInformation>
               <dateOfBirth>
                  <dateAndTimeDetails>
                     <date>01JAN60</date>
                  </dateAndTimeDetails>
               </dateOfBirth>
            </passengerData>
         </travellerInfo>
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
                  <longFreetext>DTW1S210B</longFreetext>
               </freetextData>
            </dataElementsIndiv>
            <dataElementsIndiv>
               <elementManagementData>
                  <segmentName>OP</segmentName>
               </elementManagementData>
               <optionElement>
                  <optionDetail>
                     <officeId>DTW1S210B</officeId>
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
                  <longFreetext>germain.bolanos@amadeus.com</longFreetext>
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
    response = requests.post(url, data=data_, headers=header)
    return response.content
