"""
    This is for testing purposes like a suite.
"""
import os

from pygds.amadeus.errors import ClientError, ServerError
from pygds.core.security_utils import decode_base64
from pygds.env_settings import get_setting
from pygds import log_handler
from pygds.sabre.client import SabreClient


def test():
    """ A suite of tests """

    username = get_setting("SABRE_USERNAME")
    pcc = get_setting("SABRE_PCC")
    password = decode_base64(get_setting("SABRE_PASSWPRD"))
    url = "https://webservices3.sabre.com"
    dir_path = os.path.dirname(os.path.realpath(__file__))
    log_handler.load_file_config(os.path.join(dir_path, "..", "..", "..", "log_config.yml"))
    log = log_handler.get_logger("test_all")
    pnr = "RH3WOD"  # "Q68EFX", "RI3B6D", "RT67BC"
    # m_id = None

    client = SabreClient(url, username, password, pcc, False)
    try:
        session_response = client.open_session()
        log.info(session_response)
    except ClientError as ce:
        log.error(f"client_error: {ce}")
        log.error(f"session: {ce.session_info}")
    except ServerError as se:
        log.error(f"server_error: {se}")
        log.error(f"session: {se.session_info}")


if __name__ == "__main__":
    test()
