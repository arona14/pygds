import unittest
from pygds.sabre.xmlbuilders.builder import SabreXMLBuilder



class TestTicket(unittest.TestCase):

    def setUp(self) -> None:
        self.pcc = "WR17"
        self.conversation_id = "cosmo-material-b6851be0-b83e-11e8-be20-c56b920f05b5"
        self.token = "Shared/IDL:IceSess\\/SessMgr:1\\.0.IDL/Common/!ICESMS\\/RESG!ICESMSLB\\/RES.LB!-2983077906396752768!48310!0"
        self.code_cc = "" 
        self.expire_date = ""
        self.cc_number = ""
        self.approval_code = ""
        self.commission_value = 100
        self.price_quote = 1234
        self.payment_type = "CS"
        # self.type_fop_by_credit_card = SabreXMLBuilder().info_credit_card(self.code_cc, self.expire_date, self.cc_number, self.approval_code, self.commission_value)
        self.type_fop_by_cash_or_cheque =  SabreXMLBuilder().info_cash_or_cheque(self.payment_type, self.commission_value)
 
    def test_issue_air_ticket_soap(self):
        result = SabreXMLBuilder().air_ticket_rq(self.pcc, self.token, self.type_fop_by_cash_or_cheque, self.price_quote)
        self.assertIsNotNone(result)       