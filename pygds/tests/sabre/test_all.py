"""
    This is for testing purposes like a suite.
"""
import os
from pygds.core.security_utils import decode_base64
from pygds.env_settings import get_setting
from pygds.sabre.client import SabreClient


def test():
    """ A suite of tests """

    dir_path = os.path.dirname(os.path.realpath(__file__))
    dir_path = os.path.join(dir_path, "..", "..", "..")
    os.makedirs(os.path.join(dir_path, "out"), exist_ok=True)
    # log_handler.load_file_config(os.path.join(dir_path, "log_config.yml"))
    # log = log_handler.get_logger("test_all")

    username = get_setting("SABRE_USERNAME")
    pcc = get_setting("SABRE_PCC")
    password = decode_base64(get_setting("SABRE_PASSWORD"))
    url = "https://webservices3.sabre.com"
    commission_value = """<MiscQualifiers><Commission Percent="0.00"/></MiscQualifiers>"""
    client = SabreClient(url, "", username, password, pcc, False)

    display_pnr = client.get_reservation("TLRYVS", None)
    session_info = display_pnr.session_info
    if not session_info:
        print("No session info")
        return
    message_id = session_info.message_id
    token = session_info.security_token
    # price = client.search_price_quote(message_id, retain=False, fare_type='Net', segment_select=segment_select, passenger_type=passenger_type)
    # print(price)
    remark = client.send_remark(message_id, 'Virginie')
    print(remark)
    resul_ticket = client.issue_ticket(message_id, 1, code_cc=None, expire_date=None, cc_number=None, approval_code=None, payment_type="CK", commission_value=commission_value)
    print(resul_ticket)
    result = client.end_transaction(message_id)
    print(result)


if __name__ == "__main__":
    test()
