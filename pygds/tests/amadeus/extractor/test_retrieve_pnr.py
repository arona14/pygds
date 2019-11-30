from unittest import TestCase

from pygds.amadeus.xml_parsers.retrive_pnr import GetPnrResponseExtractor

data_retrieve_pnr_p = open("pygds/tests/data/retrieve_response_p.xml")
data_retrieve_pnr_p = data_retrieve_pnr_p.read()

data_retrieve_pnr = open("pygds/tests/data/retrieve_pnr.xml")
data_retrieve_pnr = data_retrieve_pnr.read()

data_retrieve_pnr_ticket = open("pygds/tests/data/retrieve_pnr_ticket.xml")
data_retrieve_pnr_ticket = data_retrieve_pnr_ticket.read()


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

    def test_passengers(self):
        extractor = GetPnrResponseExtractor(data_retrieve_pnr_p)
        passenger = extractor.get_all_passengers[0] if extractor.get_all_passengers else None
        if passenger:
            self.assertEqual(passenger.name_id, "1")
            self.assertEqual(passenger.first_name, "A MRS")
            self.assertEqual(passenger.fore_name, "A MRS")
            self.assertEqual(passenger.passenger_type, "ADT")
            self.assertEqual(passenger.sur_name, "SMITH")

    def test_passenger_bad_response(self):
        passengers = self.extractor.get_all_passengers
        self.assertEqual(passengers, [])

    def test_price_quote(self):
        extractor = GetPnrResponseExtractor(data_retrieve_pnr)
        price_quotes = extractor.get_price_quotes[0] if extractor.get_price_quotes else None
        if price_quotes:
            self.assertEqual(price_quotes.fare_type, None)
            self.assertEqual(price_quotes.status, None)
            self.assertEqual(price_quotes.total_fare["amount"], 737.71)
            self.assertEqual(price_quotes.total_tax["amount"], 45.71)

    def test_price_quote_bad_request(self):
        price_quotes = self.extractor.get_price_quotes
        self.assertEqual(price_quotes, [])

    def test_ticketing_info(self):
        extractor = GetPnrResponseExtractor(data_retrieve_pnr_ticket)
        ticketing_infos = extractor.get_ticketing_info[0] if extractor.get_ticketing_info else None
        if ticketing_infos:
            self.assertEqual(ticketing_infos.date_time, '291119')
            self.assertEqual(ticketing_infos.full_name, 'ANDRA ')
            self.assertEqual(ticketing_infos.index, "20")
            self.assertEqual(ticketing_infos.passenger, "3")

    def test_ticketing_info_bad_request(self):
        ticketing_infos = self.extractor.get_ticketing_info
        self.assertEqual(ticketing_infos, [])

    def test_get_form_of_payment(self):
        extractor = GetPnrResponseExtractor(data_retrieve_pnr_ticket)
        form_of_payments = extractor.get_form_of_payments[0] if extractor.get_form_of_payments else None
        if form_of_payments:
            self.assertEqual(form_of_payments.card_number, 'PAX CCVIXXXXXXXXXXXX4305/1020*CVX/AAPS1OK')
            self.assertEqual(form_of_payments.card_type, 'PAX CC')
            self.assertEqual(form_of_payments.expire_month, None)
            self.assertEqual(form_of_payments.expire_year, None)

    def test_get_form_of_payment_bad_request(self):
        form_of_payments = self.extractor.get_form_of_payments
        self.assertEqual(form_of_payments, [])

    def test_get_remarks(self):
        extractor = GetPnrResponseExtractor(data_retrieve_pnr_ticket)
        get_remarks = extractor.get_remarks
        self.assertEqual(get_remarks, [])

    def test_get_remarks_bad_request(self):
        get_remarks = self.extractor.get_remarks
        self.assertEqual(get_remarks, [])


if __name__ == "__main__":
    test = TestGetPnrResponseExtractor()
    test.setUp()
    # test.test_passengers()
    # test.test_passenger_bad_response()
    # test.test_price_quote()
    # test.test_price_quote_bad_request()
    # test.test_ticketing_info()
    # test.test_ticketing_info_bad_request()
    # test.test_get_form_of_payment()
    # test.test_get_form_of_payment_bad_request()
    # test.test_get_remarks()
    # test.test_get_remarks_bad_request()
