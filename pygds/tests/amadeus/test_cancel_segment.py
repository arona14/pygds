from unittest import TestCase

from pygds.amadeus.xml_parsers.response_extractor import CancelPnrExtractor


class TestCancelPNR(TestCase):
    def setUp(self) -> None:
        self.xml = """<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:awsse="http://xml.amadeus.com/2010/06/Session_v3" xmlns:wsa="http://www.w3.org/2005/08/addressing">
                <soap:Header>
                    <wsa:To>http://www.w3.org/2005/08/addressing/anonymous</wsa:To>
                    <wsa:From>
                        <wsa:Address>https://nodeD1.test.webservices.amadeus.com/PII</wsa:Address>
                    </wsa:From>
                    <wsa:Action>http://webservices.amadeus.com/HSFREQ_07_3_1A</wsa:Action>
                    <wsa:MessageID>urn:uuid:edf933c3-fdc1-8f14-853b-9170fbb7bc3d</wsa:MessageID>
                    <wsa:RelatesTo RelationshipType="http://www.w3.org/2005/08/addressing/reply">
                        e9bd2743-8806-48f0-8a16-7c06079fff50
                    </wsa:RelatesTo>
                    <awsse:Session TransactionStatusCode="End">
                        <awsse:SessionId>Sessw</awsse:SessionId>
                        <awsse:SequenceNumber>1</awsse:SequenceNumber>
                        <awsse:SecurityToken>Tok34344e3</awsse:SecurityToken>
                    </awsse:Session>
                </soap:Header>
                <soap:Body>
                    <PNR_Reply xmlns="http://xml.amadeus.com/PNRACC_17_1_1A">
                        <pnrHeader>
                            <reservationInfo>
                                <reservation>
                                    <companyId>1A</companyId>
                                    <controlNumber>RN8UFP</controlNumber>
                                    <date>291119</date>
                                    <time>1445</time>
                                </reservation>
                            </reservationInfo>
                        </pnrHeader>
                    </PNR_Reply>
                </soap:Body>
            </soap:Envelope>"""
        self.extractor = CancelPnrExtractor(self.xml).extract()

    def test_error(self):
        self.assertEqual(self.extractor, None)


if __name__ == "__main__":
    test = TestCancelPNR()
    test.setUp()
    test.test_error()
