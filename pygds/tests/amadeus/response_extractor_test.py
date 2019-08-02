import os
from unittest import TestCase
import json

from pygds.amadeus.response_extractor import ErrorExtractor, FormOfPaymentExtractor, PricePNRExtractor, \
    CreateTstResponseExtractor
from pygds.core.price import TstInformation


class TestErrorExtractorCan(TestCase):
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
        <soap:Fault>
            <faultcode>soap:Client</faultcode>
            <faultstring>11|Session|</faultstring>
        </soap:Fault>
    </soap:Body>
</soap:Envelope>"""
        self.extractor = ErrorExtractor(self.xml)

    def test_init(self):
        extractor = ErrorExtractor(self.xml)
        self.assertIsNotNone(extractor)
        self.assertFalse(extractor.parsed, "The error extractor is parsed on init")

    def test_parse(self):
        self.extractor.parse()
        self.assertTrue(self.extractor.parsed, "The error extractor is not pared after calling .parse method")

    def test_extract(self):
        extracted = self.extractor.extract()
        self.assertIsNotNone(extracted, "The extracted error is none")
        self.assertIsNotNone(extracted.session_info)


class TestFormOfPaymentExtractor(TestCase):
    def setUp(self) -> None:
        self.xml = ""
        self.fop_extractor = FormOfPaymentExtractor(self.xml)

    def test_init(self):
        fop_extractor = FormOfPaymentExtractor(self.xml)
        self.assertIsNotNone(fop_extractor)

    def test_extract(self):
        pass


class TestTicketingExtractor(TestCase):
    pass


class TestPricePnrExtractor(TestCase):
    def setUp(self) -> None:
        base_path = os.path.dirname(os.path.abspath(__file__))
        xml_path = os.path.join(base_path, "resources/ppwbc/amadeus_price_pnr_with_booking_class_response.xml")
        json_path = os.path.join(base_path, "resources/ppwbc/amadeus_price_pnr_with_booking_class_fares.json")
        with open(xml_path) as f:
            self.xml = ''.join(f.readlines())
            self.price_extractor = PricePNRExtractor(self.xml)
        with open(json_path) as j:
            self.fare_data = json.load(j)

    def test_init(self):
        self.assertIsNotNone(self.price_extractor.xml_content)

    def test_pax_refs(self):
        refs = self.price_extractor._pax_refs(self.fare_data)
        self.assertEqual(len(refs), 1)
        self.assertEqual(refs[0], "1")

    def test_fare_amounts(self):
        amounts = self.price_extractor._amounts(self.fare_data)
        self.assertEqual(len(amounts), 3)
        self.assertEqual(amounts[0].qualifier, "B")

    def test_extract(self):
        response = self.price_extractor.extract()
        self.assertIsNotNone(response)

        session = response.session_info
        self.assertIsNotNone(session)
        self.assertFalse(session.session_ended)

        fares = response.payload
        self.assertIsNotNone(fares)
        self.assertEqual(len(fares), 1)


class TestCreateTstExtractor(TestCase):
    def setUp(self) -> None:
        base_path = os.path.dirname(os.path.abspath(__file__))
        xml_path = os.path.join(base_path, "resources/ctfp/amadeus_create_tst_from_price_response.xml")
        with open(xml_path) as f:
            self.xml = ''.join(f.readlines())
            self.tst_extractor = CreateTstResponseExtractor(self.xml)

    def test_init(self):
        self.assertIsNotNone(self.tst_extractor.xml_content)

    def test_extract(self):
        response = self.tst_extractor.extract()
        self.assertIsNotNone(response)

        session = response.session_info
        self.assertIsNotNone(session)
        self.assertFalse(session.session_ended)

        tst_info: TstInformation = response.payload
        self.assertIsNotNone(tst_info)
        self.assertEqual(tst_info.pnr, "FAKEPNR")
        self.assertEqual(tst_info.tst_reference, "3")
        self.assertEqual(tst_info.pax_references, ["2", "3"])
