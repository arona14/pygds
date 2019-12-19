from unittest import TestCase

from pygds.amadeus.xml_parsers.response_extractor import CancelPnrExtractor
from pygds.amadeus.xmlbuilders.builder import AmadeusXMLBuilder


class TestCancelPNR(TestCase):
    def setUp(self) -> None:
        self.xml = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                            xmlns:awsse="http://xml.amadeus.com/2010/06/Session_v3"
                    xmlns:wsa="http://www.w3.org/2005/08/addressing">
                    <soapenv:Header>
                        <wsa:To>http://www.w3.org/2005/08/addressing/anonymous</wsa:To>
                        <wsa:From>
                            <wsa:Address>https://nodeD1.test.webservices.amadeus.com/1ASIWCTSCSO</wsa:Address>
                        </wsa:From>
                        <wsa:Action>http://webservices.amadeus.com/PNRRET_17_1_1A</wsa:Action>
                        <wsa:MessageID>urn:uuid:1f5bdc89-97db-c904-214e-3d5e54704488</wsa:MessageID>
                        <wsa:RelatesTo RelationshipType="http://www.w3.org/2005/08/addressing/reply">0a1f818c-31be-4dde-a8f3-ebabf0a0f7d9</wsa:RelatesTo>
                        <awsse:Session TransactionStatusCode="End">
                            <awsse:SessionId>01PLTJP51N</awsse:SessionId>
                            <awsse:SequenceNumber>1</awsse:SequenceNumber>
                            <awsse:SecurityToken>WNMIELVNH6N63VM8WR44D6Z2</awsse:SecurityToken>
                        </awsse:Session>
                    </soapenv:Header>
                    <soapenv:Body>
                    <PNR_Reply xmlns="http://xml.amadeus.com/PNRACC_17_1_1A">
                        <messageActionDetails>
                            <messageFunctionDetails>
                                <messageFunction>M</messageFunction>
                            </messageFunctionDetails>
                        </messageActionDetails>
                        <information>
                            <applicationErrorInformation>
                                <applicationErrorDetail>
                                    <applicationError>1436</applicationError>
                                        <codeListQualifier>EC</codeListQualifier>
                                    <codeListResponsibleAgency>1A</codeListResponsibleAgency>
                                </applicationErrorDetail>
                            </applicationErrorInformation>
                            <interactiveFreeText>
                                <freeTextQualifier>
                                    <textSubjectQualifier>C</textSubjectQualifier>
                                    <informationType>50</informationType>
                                    <language>EN</language>
                                </freeTextQualifier>
                                <freeTextInfo>NEED NAME</freeTextInfo>
                            </interactiveFreeText>
                        </information>
                    </PNR_Reply>
                </soapenv:Body>
            </soapenv:Envelope>"""
        self.extractor = CancelPnrExtractor(self.xml).extract()
        self.builder = AmadeusXMLBuilder("", "", "", "", "")

    def test_error(self):
        self.assertNotEqual(self.extractor.payload, None)

    def test_cancel_builder(self):
        result = self.builder.cancel_segments("", "", "", "", ["2", "3"])

        self.assertNotEqual(result, None)
        self.assertIn("<number>2</number>", result)
        self.assertIn("<number>3</number>", result)


if __name__ == "__main__":
    test = TestCancelPNR()
    test.setUp()
    test.test_error()
    test.test_cancel_builder()
