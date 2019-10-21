"""
    This is for testing purposes like a suite.
"""
from pygds.core.security_utils import decode_base64
from pygds.env_settings import get_setting
from pygds.sabre.client import SabreClient


def test():
    # This is not a test file. It is just used to locally test a flow

    username = get_setting("SABRE_USERNAME")
    pcc = get_setting("SABRE_PCC")
    password = decode_base64(get_setting("SABRE_PASSWORD"))
    url = "https://webservices3.sabre.com"

    client = SabreClient(url, "", username, password, pcc, False)
    message_id = None
    client.get_or_create_session_details(message_id)


if __name__ == "__main__":
    test()
