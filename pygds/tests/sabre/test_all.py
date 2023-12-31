"""
    This is for testing purposes like a suite.
"""
# import logging
from pygds.core.security_utils import decode_base64
from pygds.env_settings import get_setting
from pygds.sabre.client import SabreClient
import os


def test():
    """ A suite of tests """

    dir_path = os.path.dirname(os.path.realpath(__file__))
    dir_path = os.path.join(dir_path, "..", "..", "..")
    os.makedirs(os.path.join(dir_path, "out"), exist_ok=True)

    username = get_setting("SABRE_USERNAME")
    pcc = get_setting("SABRE_PCC")
    password = decode_base64(get_setting("SABRE_PASSWORD"))
    url = "https://webservices3.sabre.com"

    pnr = "FAEWFW"  # "TGZKPI" "FAEWFW"
    client = SabreClient(url, "", username, password, pcc, False)
    token = None
    retrieve_pnr = client.get_reservation(token, pnr, True)
    print(retrieve_pnr)


if __name__ == "__main__":
    test()
