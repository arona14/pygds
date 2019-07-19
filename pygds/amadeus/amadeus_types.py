from pygds.core.sessions import SessionInfo


class AmadeusAddFormOfPayment:
    """
    This class is for containing information for add form of payment
    """

    def __init__(self, fop_reference_qualifier, fop_reference_number, passenger_reference_type, passenger_reference_value, fop_sequence_number, fop_pnr_details_code, fop_pnr_details_status, fop_pnr_details_edi_code, fop_pnr_details_reporting_code, fop_pnr_details_elec_ticketing_code, old_fop_free_flow_text_subject_qualifier, old_fop_free_flow_source, old_fop_free_flow_encoding, free_text, criteria_set_type, criteria_details_attribute_type, criteria_details_attribute_description, group_usage_attribute_type, payment_data_company_code, form_of_payment_type, credit_card_details_vendor_code, credit_card_details_card_number, credit_card_details_expiry_date, fortknox_ids_type, fortknox_ids_value):
        self.fop_reference_qualifier = fop_reference_qualifier
        self.fop_reference_number = fop_reference_number
        self.passenger_reference_type = passenger_reference_type
        self.passenger_reference_value = passenger_reference_value
        self.fop_sequence_number = fop_sequence_number
        self.fop_pnr_details_code = fop_pnr_details_code
        self.fop_pnr_details_status = fop_pnr_details_status
        self.fop_pnr_details_edi_code = fop_pnr_details_edi_code
        self.fop_pnr_details_reporting_code = fop_pnr_details_reporting_code
        self.fop_pnr_details_elec_ticketing_code = fop_pnr_details_elec_ticketing_code
        self.old_fop_free_flow_text_subject_qualifier = old_fop_free_flow_text_subject_qualifier
        self.old_fop_free_flow_source = old_fop_free_flow_source
        self.old_fop_free_flow_encoding = old_fop_free_flow_encoding
        self.free_text = free_text
        self.criteria_set_type = criteria_set_type
        self.criteria_details_attribute_type = criteria_details_attribute_type
        self.criteria_details_attribute_description = criteria_details_attribute_description
        self.group_usage_attribute_type = group_usage_attribute_type
        self.payment_data_company_code = payment_data_company_code
        self.form_of_payment_type = form_of_payment_type
        self.credit_card_details_vendor_code = credit_card_details_vendor_code
        self.credit_card_details_card_number = credit_card_details_card_number
        self.credit_card_details_expiry_date = credit_card_details_expiry_date
        self.fortknox_ids_type = fortknox_ids_type
        self.fortknox_ids_value = fortknox_ids_value

    def __repr__(self):
        return {
            "fop_reference_qualifier": self.fop_reference_qualifier,
            "fop_reference_number": self.fop_reference_number,
            "passenger_reference_type": self.passenger_reference_type,
            "passenger_reference_value": self.passenger_reference_value,
            "fop_sequence_number": self.fop_sequence_number,
            "fop_pnr_details_code": self.fop_pnr_details_code,
            "fop_pnr_details_status": self.fop_pnr_details_status,
            "fop_pnr_details_edi_code": self.fop_pnr_details_edi_code,
            "fop_pnr_details_reporting_code": self.fop_pnr_details_reporting_code,
            "fop_pnr_details_elec_ticketing_code": self.fop_pnr_details_elec_ticketing_code,
            "old_fop_free_flow_text_subject_qualifier": self.old_fop_free_flow_text_subject_qualifier,
            "old_fop_free_flow_source": self.old_fop_free_flow_source,
            "old_fop_free_flow_encoding": self.old_fop_free_flow_encoding,
            "free_text": self.free_text,
            "criteria_set_type": self.criteria_set_type,
            "criteria_details_attribute_type": self.criteria_details_attribute_type,
            "criteria_details_attribute_description": self.criteria_details_attribute_description,
            "group_usage_attribute_type": self.group_usage_attribute_type,
            "payment_data_company_code": self.payment_data_company_code,
            "form_of_payment_type": self.form_of_payment_type,
            "credit_card_details_vendor_code": self.credit_card_details_vendor_code,
            "credit_card_details_card_number": self.credit_card_details_card_number,
            "credit_card_details_expiry_date": self.credit_card_details_expiry_date,
            "fortknox_ids_type": self.fortknox_ids_type,
            "fortknox_ids_value": self.fortknox_ids_value
        }

    def __str__(self):
        return str(self.__repr__())


class AmadeusAddMultiElement:
    """
    This class is for containing information for add multi element
    """

    def __init__(self, response):
        self.response = response

    def __repr__(self):
        return {"response": self.response}

    def __str__(self):
        return str(self.__repr__())


class AmadeusTicketing:
    """
    : This class is for containing information for the response add ticketing
    : It returns an object with the ticket number with the key freetext
    : And an error_code ok if all is done
    """

    def __init__(self, status_code, error_code, text_subject_qualifier, source, encoding, freetext):
        self.status_code = status_code
        self.error_code = error_code
        self.text_subject_qualifier = text_subject_qualifier
        self.source = source
        self.encoding = encoding
        self.freetext = freetext

    def __repr__(self):
        return {
            "status_code": self.status_code,
            "error_code": self.error_code,
            "text_subject_qualifier": self.text_subject_qualifier,
            "source": self.source,
            "encoding": self.encoding,
            "freetext": self.freetext
        }

    def __str__(self):
        return str(self.__repr__())


class GdsResponse:
    """
    This class is for holding a parsed response from GDS. It will include the session information and the useful data (payload)
    """

    def __init__(self, session_info: SessionInfo, payload=None):
        self.session_info = session_info
        self.payload = payload
