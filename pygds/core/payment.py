class FormOfPayment:
    """
    A polymorphic class to hold a form of payment
    """

    def __init__(self, p_code, p_type, company_code):
        self.p_code = p_code
        self.p_type = p_type
        self.company_code = company_code

    def is_valid(self):
        return True


class CreditCard(FormOfPayment):
    """
    A credit card as form of payment
    """

    def __init__(self, company_code, vendor_code, card_number, security_id, approval_code, expiry_date):
        super().__init__("CCVI", "CC", company_code)
        self.vendor_code = vendor_code
        self.card_number = card_number
        self.security_id = security_id
        self.approval_code = approval_code
        self.expiry_date = expiry_date

    def is_valid(self):
        return self.vendor_code and self.expiry_date and self.card_number


class CheckPayment(FormOfPayment):
    def __init__(self, p_code: str = None, company_code: str = None):
        FormOfPayment.__init__(self, p_code, "CK", company_code)


class CqCheckPayment(FormOfPayment):
    def __init__(self, p_code: str = None, company_code: str = None):
        FormOfPayment.__init__(self, p_code, "CQ", company_code)


class ChashPayment(FormOfPayment):
    def __init__(self, p_code: str = None, company_code: str = None):
        super().__init__(p_code, "CA", company_code)
