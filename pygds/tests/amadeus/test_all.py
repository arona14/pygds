"""
    This is for testing purposes like a suite.
"""

import os
from pygds.amadeus.client import AmadeusClient
from pygds.amadeus.errors import ClientError, ServerError
from pygds.env_settings import get_setting
from pygds import log_handler


def test():
    """ A suite of tests """
    endpoint = get_setting("AMADEUS_ENDPOINT_URL")
    username = get_setting("AMADEUS_USERNAME")
    password = get_setting("AMADEUS_PASSWORD")
    office_id = get_setting("AMADEUS_OFFICE_ID")
    wsap = get_setting("AMADEUS_WSAP")
    vendor_code = "CA"
    carte_number = "5100290029002909"
    security_id = "737"
    expiry_date = "1020"
    form_of_payment = "FP"
    passenger_reference_type = "PT"
    passenger_reference_value = "1"
    form_of_payment_sequence_number = "1"
    form_of_payment_code = "CCVI"
    group_usage_attribute_type = "FP"
    company_code = "LO"
    form_of_payment_type = "CC"
    dir_path = os.path.dirname(os.path.realpath(__file__))
    log_handler.load_file_config(os.path.join(dir_path, "..", "..", "..", "log_config.yml"))
    log = log_handler.get_logger("test_all")

    client = AmadeusClient(endpoint, username, password, office_id, wsap, True)
    try:
        #session_info = client.start_new_session()
       # print(session_info)
        res = client.get_reservation(office_id, None, None, 'Q68EFX', True)
       # res = client.add_form_of_payment(office_id, session_info.session_id, session_info.sequence_number, session_info.security_token, form_of_payment, passenger_reference_type, passenger_reference_value, form_of_payment_sequence_number, form_of_payment_code, group_usage_attribute_type, company_code, form_of_payment_type, vendor_code, carte_number, security_id, expiry_date)
       # res = client.ticketing_pnr("ConvId", session_info.session_id, session_info.sequence_number, session_info.security_token, passenger_reference_type, passenger_reference_value)
        #res = client.fare_master_pricer_travel_board_search("PAR", "WAW", "050819", "100819")
        #res = client.fare_price_pnr_with_booking_class("WbsConsu-BKqflYaGY0WAgxkCQ00ACBQ20GM3Jit-Yhnyfq1dH", session_info.session_id, "4", session_info.security_token)
        print(str(res))
        s_id, seq, tok, m_id = (None, None, None, None)
        pnr = "Q68EFX"
        res_command = client.send_command(f"RT{pnr}", m_id, s_id, seq, tok)
        session_info, command_response = (res_command.session_info, res_command.payload)
        log.info(session_info)
        log.info(command_response)
        res_command = client.send_command(f"IR", m_id, s_id, seq, tok)
        session_info, command_response = (res_command.session_info, res_command.payload)
        log.info(session_info)
        log.info(command_response)
    except ClientError as ce:
        log.error(f"client_error: {ce}")
        log.error(f"session: {ce.session_info}")
    except ServerError as se:
        log.error(f"server_error: {se}")
        log.error(f"session: {se.session_info}")


if __name__ == "__main__":
    test()
