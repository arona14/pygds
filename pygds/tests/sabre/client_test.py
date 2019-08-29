import unittest
from pygds.sabre.client import SabreClient
from pygds.env_settings import get_setting
from pygds.core.security_utils import decode_base64
from pygds.sabre.xmlbuilders.builder import SabreXMLBuilder


class ClientCan(unittest.TestCase):
    """ This class will test all our function on the client side """

    def setUp(self) -> None:
        self.pcc = get_setting("SABRE_PCC")
        self.username = get_setting("SABRE_USERNAME")
        self.password = decode_base64(get_setting("SABRE_PASSWORD"))
        self.rest_url = "https://api.havail.sabre.com"
        self.soap_url = "https://webservices3.sabre.com"
        self.pnr = "CYHCFQ"
        self.xml_builder = SabreXMLBuilder(self.soap_url, self.username, self.password, self.pcc)
        self.client = SabreClient(self.soap_url, self.rest_url, self.username, self.password, self.pcc, False)
        self.token = (self.client.get_reservation(self.pnr, None)).session_info.security_token
        self.message_id = (self.client.get_reservation(self.pnr, None)).session_info.message_id
        self.pcc = "WR17"
        self.code_cc = ""
        self.expire_date = ""
        self.cc_number = ""
        self.approval_code = ""
        self.commission_value = """<MiscQualifiers><Commission Percent="0.00"/></MiscQualifiers>"""
        self.price_quote = 1
        self.payment_type = "CK"
        self.type_fop_by_credit_card = self.xml_builder.fop_choice(self.code_cc, self.expire_date, self.cc_number, self.payment_type)
        self.type_fop_by_cash_or_cheque = self.xml_builder.fop_choice(self.payment_type, self.commission_value)

    def test_soap_request_wrapper(self):
        session = self.client._soap_request_wrapper("None")
        self.assertIsNotNone(session, "The result of open session token is None")

    def test_issue_ticket(self):
        result = self.client.issue_ticket(self.message_id, self.price_quote, self.payment_type, self.commission_value)
        self.assertIsNotNone(result, "Cannot issue ticket")
        # self.assertIsNotNone(result.payload.status)
        # self.assertTrue(isinstance(result.payload.status), str)
        # self.assertEquals(result.payload.status, "Complete")

    def test_end_transaction(self):
        result = self.client.end_transaction(self.message_id)
        self.assertIsNotNone(result, "Cannot end the transaction")
        # self.assertIsNotNone(result.payload)
        # self.assertTrue(isinstance(result.payload.status), str)
        # self.assertTrue(isinstance(result.payload.id_ref), str)
        # self.assertTrue(isinstance(result.payload.create_date_time), str)
        # self.assertTrue(isinstance(result.payload.text_message), str)
        # self.assertEquals(result.payload.status, "Complete")

    def test_send_command(self):
        result = self.client.send_command(self.message_id, "*DJICXH")
        self.assertIsNotNone(result, "Cannot sent command")

    def test_get_reservation(self):
        result = self.client.get_reservation(self.pnr, None)
        self.assertIsNotNone(result, "Cannot retrieve pnr")

    def test_queue_place(self):
        result = self.client.queue_place(self.token, 111, self.pnr)
        self.assertIsNotNone(result.payload.status)
        self.assertIsNotNone(result.payload.type_response)
        self.assertIsNotNone(result.payload.text_message)
        self.assertEquals(result.payload.status, "Complete")
        self.assertEquals(result.payload.type_response, "Success")


if __name__ == "__main__":
    unittest.main()
