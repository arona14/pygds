import requests
from security_utils import generate_nonce,generate_created,password_digest
from xmlbuilders.builder import AmadeusXMLBuilder
from env_settings_ import get_setting

class AmadeusTicketing:
    """This class allows the process of ticketing by using a set of functions such as add_form_of_payment() 
    this adds to the pnr forms of payment for each passenger. It takes into parameter the pnr, 
    the form of payment (cash, credit card, check and transfer), id of the passenger ...
    the function ticketing() manages the ticketing part taking into account the passenger's id and its type"""

    def add_form_of_payment(self, message_id, session_id, sequence_number, security_token, form_of_payment, passenger_reference_type, passenger_reference_value, form_of_payment_sequence_number, form_of_payment_code, group_usage_attribute_type, company_code, form_of_payment_type, vendor_code, carte_number, security_id, expiry_date):
        try:
            token_session = "2I2R99GX9MUSP7UNGQ7EIZYJ6"
            url = "https://nodeD1.test.webservices.amadeus.com"
            header = {'Content-Type': 'text/xml;charset=UTF-8', 'Accept-Encoding': 'gzip,deflate', 'SOAPAction': 'http://webservices.amadeus.com/TFOPCQ_15_4_1A'}
            endpoint = get_setting("AMADEUS_ENDPOINT_URL")
            username = get_setting("AMADEUS_USERNAME")
            password = get_setting("AMADEUS_PASSWORD")
            office_id = "DTW1S210B"
            wsap = get_setting("AMADEUS_WSAP")
            add_fop = AmadeusXMLBuilder(endpoint, username, password, office_id, wsap).add_form_of_payment(message_id, session_id, sequence_number, security_token, form_of_payment, passenger_reference_type, passenger_reference_value, form_of_payment_sequence_number, form_of_payment_code, group_usage_attribute_type, company_code, form_of_payment_type, vendor_code, carte_number, security_id, expiry_date)
            response = requests.post(url, data=add_fop, headers=header)
            print(response.content)
            status_code = response.status_code
        except Exception as e:
            print(e)
            # TODO: Capture the real exception not the general one
            raise e
        return status_code

    def tiketing(self, message_id, session_id, sequence_number, security_token, passenger_reference_type, passenger_reference_value):
        try:
            token_session = "2I2R99GX9MUSP7UNGQ7EIZYJ6"
            url = "https://nodeD1.test.webservices.amadeus.com"
            header = {'Content-Type': 'text/xml;charset=UTF-8', 'Accept-Encoding': 'gzip,deflate', 'SOAPAction': 'http://webservices.amadeus.com/TTKTIQ_15_1_1A'}
            endpoint = get_setting("AMADEUS_ENDPOINT_URL")
            username = get_setting("AMADEUS_USERNAME")
            password = get_setting("AMADEUS_PASSWORD")
            office_id = "DTW1S210B"
            wsap = get_setting("AMADEUS_WSAP")
            ticket_res = AmadeusXMLBuilder(endpoint, username, password, office_id, wsap).add_ticket_pnr(message_id, session_id, sequence_number, security_token, passenger_reference_type, passenger_reference_value)
            response = requests.post(url, data=ticket_res, headers=header)
            print(response.status_code)
            status_code = response.content
        except Exception as e:
            print(e)
            raise e
        return status_code        

# df test():
message_id = "S32B6N"
session_id = "001M3SSTV1"
pnr = "S32B6N"
security_token = "2I2R99GX9MUSP7UNGQ7EIZYJ6"
compagniId = "1A"
agenceId = "FMSU"
vendor_code = "CA"
carte_number = "5100290029002909"
security_id = "737"
expiry_date = "1020"
form_of_payment = "FP"
passenger_reference_type = "PT"
passenger_reference_value = "3"
form_of_payment_sequence_number = "1"
form_of_payment_code = "CCVI"
group_usage_attribute_type = "FP"
company_code = "LO"
form_of_payment_type = "CC"
sequence_number = "1"


#print(AmadeusTicketing().add_form_of_payment(message_id, session_id, sequence_number, security_token, form_of_payment, passenger_reference_type, passenger_reference_value, form_of_payment_sequence_number, form_of_payment_code, group_usage_attribute_type, company_code, form_of_payment_type, vendor_code, carte_number, security_id, expiry_date))

print(AmadeusTicketing().tiketing(message_id, session_id, sequence_number, security_token, passenger_reference_type, passenger_reference_value))
# if __name__ == "__main__":
#     test()
