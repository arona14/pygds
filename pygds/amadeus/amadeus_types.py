class AmadeusSessionInfo:
    """
    This class is for containing information for a session
    """
    def __init__(self, security_token, sequence_number, session_id):
        self.security_token = security_token
        self.sequence_number = sequence_number
        self.session_id = session_id

    def __repr__(self):
        return {
            "security_token": self.security_token,
            "sequence_number": self.sequence_number,
            "session_id": self.session_id
        }

    def __str__(self):
        return str(self.__repr__())

class AmadeusAddFormOfPayment:
    """
    This class is for containing information for add form of payment
    """
    def __init__(self, fop_reference_qualifier, fop_reference_number, passenger_reference_type, passenger_reference_value, fop_sequence_number, fop_pnr_details_code, fop_pnr_details_status, fop_pnr_details_edi_code, fop_pnr_details_reporting_code, fop_pnr_details_elec_ticketing_code, old_fop_free_flow_text_subject_qualifier, old_fop_free_flow_source, old_fop_free_flow_encoding, free_text, criteria_set_type, criteria_details_attribute_type, criteria_details_attribute_description):
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
            "criteria_details_attribute_description": self.criteria_details_attribute_description
        }
    
    def __str__(self):
        return str(self.__repr__())