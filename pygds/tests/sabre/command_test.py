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

    client = SabreClient(url, username, password, pcc, False)

    display_pnr = client.get_reservation("KDDLRA", None)
    sabre_command = client.send_command(display_pnr.session_info.message_id, "*KDDLRA")
    return sabre_command


if __name__ == "__main__":
    print(test())
