from unittest import TestCase
from pygds.core.security_utils import decode_base64
from pygds.env_settings import get_setting
from pygds.sabre.client import SabreClient

class TestTicket(TestCase):

    def setUp(self) -> None:
        self.username = get_setting("SABRE_USERNAME")
        self.pcc = get_setting("SABRE_PCC")
        self.password = decode_base64(get_setting("SABRE_PASSWORD"))
        self.url = "https://webservices3.sabre.com"
        self.pnr = "DJICXH"
        self.client = SabreClient(self.url, self.username, self.password, self.pcc, False)
        self.token = (self.client.get_reservation(self.pnr, None)).session_info.security_token
        self.pcc = "WR17"
        self.code_cc = ""
        self.expire_date = ""
        self.cc_number = ""
        self.approval_code = ""
        self.commission_value = """<MiscQualifiers><Commission Percent="0.00"/></MiscQualifiers>"""
        self.price_quote = 1
        self.payment_type = "CK"
        self.type_fop_by_credit_card = self.client.fop_choice(self.code_cc, self.expire_date, self.cc_number, self.payment_type)
        self.type_fop_by_cash_or_cheque = self.client.fop_choice(self.payment_type, self.commission_value)

    def test_issue_ticket(self):
        result = self.client.issue_ticket(self.token, self.price_quote, self.type_fop_by_cash_or_cheque, self.commission_value)
        self.assertIsNotNone(result, "Cannot issue ticket")    