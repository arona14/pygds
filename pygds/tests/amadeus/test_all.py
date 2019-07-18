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
    dir_path = os.path.dirname(os.path.realpath(__file__))
    log_handler.load_file_config(os.path.join(dir_path, "..", "..", "..", "log_config.yml"))
    log = log_handler.get_logger("test_all")

    client = AmadeusClient(endpoint, username, password, office_id, wsap, True)
    try:
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
