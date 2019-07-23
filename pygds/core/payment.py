class FormOfPayment:
    """
    A polymorphic class to hold a form of payment
    """
    def __init__(self, p_code, p_type, company_code):
        self.p_code = p_code
        self.p_type = p_type
        self.company_code = company_code


class CreditCard(FormOfPayment):
    """
    A credit card as form of payment
    """
    def __init__(self, company_code, vendor_code, card_number, security_id, expiry_date):
        super().__init__("", "", company_code)  # TODO: complete with exact type and code
        self.vendor_code = vendor_code
        self.card_number = card_number
        self.security_id = security_id
        self.expiry_date = expiry_date
