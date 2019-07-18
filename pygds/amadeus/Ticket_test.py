# import requests
# def test():
#     return f"""
# <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:sec="http://xml.amadeus.com/2010/06/Security_v1" xmlns:typ="http://xml.amadeus.com/2010/06/Types_v1" xmlns:iat="http://www.iata.org/IATA/2007/00/IATA2010.1" xmlns:app="http://xml.amadeus.com/2010/06/AppMdw_CommonTypes_v3" xmlns:link="http://wsdl.amadeus.com/2010/06/ws/Link_v1" xmlns:ses="http://xml.amadeus.com/2010/06/Session_v3">
#    <soapenv:Header xmlns:add="http://www.w3.org/2005/08/addressing">
# 	<add:MessageID>WbsConsu-njU8WwJrBMMwDroHODh1EDr4sJZPw57-uWfq8M4HE</add:MessageID>
# 	<add:Action>http://webservices.amadeus.com/TTKTIQ_15_1_1A</add:Action>
# 	<add:To>https://nodeD1.test.webservices.amadeus.com/1ASIWCTSCSO</add:To>
# 	<awsse:Session TransactionStatusCode="InSeries" xmlns:awsse="http://xml.amadeus.com/2010/06/Session_v3">
# 		<awsse:SessionId>0036L21Q69</awsse:SessionId>
# 		<awsse:SequenceNumber>1</awsse:SequenceNumber>
# 		<awsse:SecurityToken>N98E2AB0A5E1VON4KPQT3QUQ</awsse:SecurityToken>
# 	</awsse:Session>
# </soapenv:Header>
#    <soapenv:Body>
#       <DocIssuance_IssueTicket>
#          <optionGroup>
#             <switches>
#                <statusDetails>
#                   <indicator>RT</indicator>
#                </statusDetails>
#             </switches>
#          </optionGroup>
#       </DocIssuance_IssueTicket>
#    </soapenv:Body>
# </soapenv:Envelope>"""

# def send():
#     url_ = "https://nodeD1.test.webservices.amadeus.com"
#     header = {'Content-Type': 'text/xml;charset=UTF-8', 'Accept-Encoding': 'gzip,deflate', 'SOAPAction': 'http://webservices.amadeus.com/TTKTIQ_15_1_1A'}
#     data_ = test()
#     res = requests.post(url=url_, data=data_, headers=header)
#     print(res.content)
#     status_code = res.status_code
#     return status_code


# print(send())
