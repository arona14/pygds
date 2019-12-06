from unittest import TestCase

from pygds.amadeus.xml_parsers.retrive_pnr_v_fnc import GetPnrResponseExtractor

data_retrieve_pnr_p = open("pygds/tests/data/retrieve_response_p.xml")
data_retrieve_pnr_p = data_retrieve_pnr_p.read()

data_retrieve_pnr = open("pygds/tests/data/retrieve_pnr.xml")
data_retrieve_pnr = data_retrieve_pnr.read()

data_retrieve_pnr_ticket = open("pygds/tests/data/retrieve_pnr_ticket.xml")
data_retrieve_pnr_ticket = data_retrieve_pnr_ticket.read()

retrieve_pnr = open("pygds/tests/data/retreive_pnr_PFU66D.xml")
retrieve_pnr = retrieve_pnr.read()


class TestGetPnrResponseExtractor(TestCase):
    def setUp(self):
        self.extractor = GetPnrResponseExtractor("""<?xml version="1.0"?>
                <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                    xmlns:awsse="http://xml.amadeus.com/2010/06/Session_v3"
                    xmlns:wsa="http://www.w3.org/2005/08/addressing">
                    <soapenv:Header>
                        <wsa:To>http://www.w3.org/2005/08/addressing/anonymous</wsa:To>
                        <wsa:From>
                            <wsa:Address>https://nodeD1.test.webservices.amadeus.com/1ASIWCTSCSO</wsa:Address>
                        </wsa:From>
                        <wsa:Action>http://webservices.amadeus.com/PNRADD_17_1_1A</wsa:Action>
                        <wsa:MessageID>urn:uuid:e75d946f-8b7e-ef24-f9c5-329f4e69de89</wsa:MessageID>
                        <wsa:RelatesTo RelationshipType="http://www.w3.org/2005/08/addressing/reply">653504c8-8e8f-4a94-959d-cbcf95dd05ac</wsa:RelatesTo>
                        <awsse:Session TransactionStatusCode="InSeries">
                            <awsse:SessionId>00BJ8D68SK</awsse:SessionId>
                            <awsse:SequenceNumber>6</awsse:SequenceNumber>
                            <awsse:SecurityToken>1QKGJOJ1RIZFP1FXSX398UUWP9</awsse:SecurityToken>
                        </awsse:Session>
                    </soapenv:Header>
                    <soapenv:Body>
                        <PNR_Reply xmlns="http://xml.amadeus.com/PNRACC_17_1_1A">
                        </PNR_Reply>
                    </soapenv:Body>
                </soapenv:Envelope>""")
        self.extractor_data_retrieve_pnr_p = GetPnrResponseExtractor(data_retrieve_pnr_p)
        self.extractor_data_retrieve_pnr = GetPnrResponseExtractor(data_retrieve_pnr)
        self.extractor_data_retrieve_pnr_ticket = GetPnrResponseExtractor(data_retrieve_pnr_ticket)
        self.extract_retreive_pnr = GetPnrResponseExtractor(retrieve_pnr)

    def test_passengers(self):
        extractor = self.extractor_data_retrieve_pnr_p.get_all_passengers
        passenger = extractor[0] if extractor else None
        if passenger:
            self.assertEqual(passenger.name_id, "1")
            self.assertEqual(passenger.first_name, "A MRS")
            self.assertEqual(passenger.fore_name, "A MRS")
            self.assertEqual(passenger.passenger_type, "ADT")
            self.assertEqual(passenger.sur_name, "SMITH")

    def test_gender_passenger(self):
        passengers = self.extract_retreive_pnr.get_all_passengers
        if passengers:
            for passenger in passengers:
                self.assertIsNotNone(passenger.date_of_birth)

    def test_passenger_bad_response(self):
        passengers = self.extractor.get_all_passengers
        self.assertEqual(passengers, [])

    def test_price_quote(self):
        extractor = self.extractor_data_retrieve_pnr.get_price_quotes
        price_quotes = extractor[0] if extractor else None
        if price_quotes:
            self.assertEqual(price_quotes.fare_type, None)
            self.assertEqual(price_quotes.status, None)
            self.assertEqual(price_quotes.total_fare["amount"], 737.71)
            self.assertEqual(price_quotes.total_tax["amount"], 45.71)

    def test_price_quote_bad_request(self):
        price_quotes = self.extractor.get_price_quotes
        self.assertEqual(price_quotes, [])

    def test_ticketing_info(self):
        extractor = self.extractor_data_retrieve_pnr_ticket.get_ticketing_info
        ticketing_infos = extractor[0] if extractor else None
        if ticketing_infos:
            self.assertEqual(ticketing_infos.date_time, '291119')
            self.assertIsNotNone(ticketing_infos.ticket_number)
            self.assertEqual(ticketing_infos.index, "20")
            self.assertEqual(ticketing_infos.passenger, "3")

    def test_ticketing_info_bad_request(self):
        ticketing_infos = self.extractor.get_ticketing_info
        self.assertEqual(ticketing_infos, [])

    def test_get_form_of_payment(self):
        extractor = self.extractor_data_retrieve_pnr_ticket.get_form_of_payments
        form_of_payments = extractor[0] if extractor else None
        if form_of_payments:
            self.assertEqual(form_of_payments.card_number, 'XXXXXXXXXXXX4305')
            self.assertEqual(form_of_payments.card_type, 'CC')
            self.assertEqual(form_of_payments.expire_month, '10')
            self.assertEqual(form_of_payments.expire_year, '20')

    def test_get_form_of_payment_bad_request(self):
        form_of_payments = self.extractor.get_form_of_payments
        self.assertEqual(form_of_payments, [])

    def test_get_remarks(self):

        get_remarks = self.extractor_data_retrieve_pnr_ticket.get_remarks
        self.assertEqual(get_remarks, [])

    def test_get_remarks_bad_request(self):
        get_remarks = self.extractor.get_remarks
        self.assertEqual(get_remarks, [])

    def test_get_segments(self):
        extractor = self.extractor_data_retrieve_pnr_ticket.get_segments
        segments = extractor[0] if extractor else None
        if segments:
            self.assertEqual(len(segments.segments), 1)
            self.assertEqual(segments.segments[0].action_code, 'HK')
            self.assertEqual(segments.segments[0].sequence, "1")

    def test_get_segments_bad_request(self):
        segments = self.extractor.get_segments
        self.assertEqual(segments, [])


if __name__ == "__main__":
    test = TestGetPnrResponseExtractor()
    test.setUp()
    test.test_passengers()
    test.test_passenger_bad_response()
    test.test_gender_passenger()
    test.test_price_quote()
    test.test_price_quote_bad_request()
    test.test_ticketing_info()
    test.test_ticketing_info_bad_request()
    test.test_get_form_of_payment()
    test.test_get_form_of_payment_bad_request()
    test.test_get_remarks()
    test.test_get_remarks_bad_request()
    test.test_get_segments()
    test.test_get_segments_bad_request()
