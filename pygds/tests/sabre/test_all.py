"""
    This is for testing purposes like a suite.
"""

from pygds.core.security_utils import decode_base64
from pygds.env_settings import get_setting
from pygds.sabre.client import SabreClient


def test():
   """ A suite of tests """
   username = get_setting("SABRE_USERNAME")
   pcc = get_setting("SABRE_PCC")
   password = decode_base64(get_setting("SABRE_PASSWORD"))
   url = "https://webservices3.sabre.com"
   commission_value = """<MiscQualifiers><Commission Percent="0.00"/></MiscQualifiers>"""

   client = SabreClient(url, username, password, pcc, False)

   segment_select = [1, 2, 3, 4]
   passenger_type = [
        {
            "code": "JCB",
            "nameSelect": [
                "01.01"
            ],
            "quantity": 1
        },
        {
            "code": "JCB",
            "nameSelect": [
                "02.01"
            ],
            "quantity": 1
        },
        {
            "code": "J11",
            "nameSelect": [
                "03.01"
            ],
            "quantity": 1
        },
        {
            "code": "JNF",
            "nameSelect": [
                "04.01"
            ],
            "quantity": 1
        }
    ]
   display_pnr = client.get_reservation("DJICXH", None)
   session_info = display_pnr.session_info

   if not session_info:
      print("Awma session info")
      return
   message_id = session_info.message_id
   token = session_info.security_token
   price = client.search_price_quote(message_id, retain=False, fare_type='Net', segment_select=segment_select, passenger_type=passenger_type)
   print(price.application_error.description)

   result = client.issue_ticket(token, 1, code_cc = None, expire_date = None, cc_number = None, approval_code = None, payment_type = "CK", commission_value = commission_value)
   print(result.application_error.description)

   result = client.end_transaction(token)
   print(result.application_error.description)

if __name__ == "__main__":
    test()
