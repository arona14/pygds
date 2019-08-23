"""
    This is for testing purposes like a suite.
"""
import os
from pygds.amadeus.errors import ClientError, ServerError
from pygds.core.security_utils import decode_base64
from pygds.env_settings import get_setting
from pygds import log_handler
from pygds.sabre.client import SabreClient
import time,sqlite3,json
from os import getcwd,chdir,mkdir


def test():
    """ A suite of tests """

    username = get_setting("SABRE_USERNAME")
    pcc = get_setting("SABRE_PCC")
    password = decode_base64(get_setting("SABRE_PASSWORD"))
    url = "https://webservices3.sabre.com"
 
    client = SabreClient(url, username, password, pcc, False)

    display_pnr = client.get_reservation("KDDLRA", None)
    return display_pnr

if __name__ == "__main__":
    print(test())
