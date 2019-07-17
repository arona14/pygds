"""
    This is for testing purposes like a suite.
"""

import os
# from pygds.amadeus.amadeus_types import AmadeusSessionInfo
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
    dir_path = os.path.dirname(os.path.realpath(__file__))
    log_handler.load_file_config(os.path.join(dir_path, "..", "..", "..", "log_config.yml"))
    log = log_handler.get_logger("test_all")

    client = AmadeusClient(endpoint, username, password, office_id, wsap, True)
    try:
        # session_info: AmadeusSessionInfo = client.end_session("1444d25f-6a41-453d-b470-40b11800b1c4", "0040OA0Z0U", "2", "18S22N1IEJ6AX4DW6X7U04RJ9")
        # session_info: AmadeusSessionInfo = client.start_new_session()
        # print(session_info)
        # # s_id, seq, tok, m_id = ("01QRI3RJ49", "2", "3HYKHH9PY33Q2PUMO2PCZTLK2", "Test-me")
        # sess, search = client.fare_master_pricer_travel_board_search("PAR", "WAW", "050819", "100819")
        # s_id, seq, tok, m_id = (sess.session_id, sess.sequence_number, sess.security_token, sess.message_id)
        s_id, seq, tok, m_id = (None, None, None, None)
        # s_id, seq, tok, m_id = ("01R2UJ60FW", "3", "2DLL3YL8ZO5KJHV3SR88J33F5", "WbsConsu-8avfVe16eb9d45D4UXEgm35mIJGhtia-Pb4V00Rhb")
        pnr = "Q68EFX"
        res_command = client.send_command(f"RT{pnr}", m_id, s_id, seq, tok)
        session_info, command_response = (res_command.session_info, res_command.payload)
        log.info(session_info)
        log.info(command_response)
        res_command = client.send_command(f"IR", m_id, s_id, seq, tok)
        session_info, command_response = (res_command.session_info, res_command.payload)
        log.info(session_info)
        log.info(command_response)
        # s_id, seq, tok, m_id = (session_info.session_id, session_info.sequence_number, session_info.security_token, session_info.message_id)
        # client.end_session(m_id, s_id, seq, tok)
        # s_id, seq, tok, m_id = (session_info.session_id, int(session_info.sequence_number) + 1, session_info.security_token, session_info.message_id)
        # command_response, _ = client.send_command(f"IR", m_id, s_id, seq, tok)
        # print(command_response)
        # # res = client.fare_master_pricer_travel_board_search("PAR", "WAW", "050819", "100819")
        # # res = client.fare_price_pnr_with_booking_class("WbsConsu-BKqflYaGY0WAgxkCQ00ACBQ20GM3Jit-Yhnyfq1dH", session_info.session_id, "4", session_info.security_token)
        # # print(str(res))
    except ClientError as ce:
        log.error(f"client_error: {ce}")
        log.error(f"session: {ce.session_info}")
    except ServerError as se:
        log.error(f"server_error: {se}")
        log.error(f"session: {se.session_info}")


if __name__ == "__main__":
    test()
