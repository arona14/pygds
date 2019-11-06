"""
    This is for testing purposes like a suite.
"""
import logging

from pygds import log_handler
from pygds.core.security_utils import decode_base64
from pygds.env_settings import get_setting
from pygds.sabre.client import SabreClient
import os


def test():
    """ A suite of tests """

    dir_path = os.path.dirname(os.path.realpath(__file__))
    dir_path = os.path.join(dir_path, "..", "..", "..")
    os.makedirs(os.path.join(dir_path, "out"), exist_ok=True)
    log_handler.load_file_config(os.path.join(dir_path, "log_config.yml"))
    log = log_handler.get_logger("test_all")

    username = get_setting("SABRE_USERNAME")
    pcc = get_setting("SABRE_PCC")
    password = decode_base64(get_setting("SABRE_PASSWORD"))
    url = "https://webservices3.sabre.com"
    pnr = "GOQOBU"  # "TGZKPI"
    second_pnr = "TGZKPI"
    client = SabreClient(url, "", username, password, pcc, False)
    token = None

    log.info(f"------------------ Retrieve PNR {pnr}--------------")
    retrieve_pnr = client.get_reservation(token, True, pnr)
    log.debug(retrieve_pnr)
    closed = retrieve_pnr.session_info.session_ended
    if closed is True:
        log.info("Session already closed")
        return

    log.info(f"------------------ Retrieve PNR {second_pnr}--------------")
    token = retrieve_pnr.session_info.security_token
    retrieve_pnr = client.get_reservation(token, True, second_pnr)
    log.debug(retrieve_pnr)
    closed = retrieve_pnr.session_info.session_ended
    if closed is False:
        client.close_session(retrieve_pnr.session_info.security_token)


if __name__ == "__main__":
    test()
"Shared/IDL:IceSess\\\\/SessMgr:1\\\\.0.IDL/Common/!ICESMS\\\\/RESB!ICESMSLB\\\\/RES.LB!-2955511136615197053!533177!0"
"Shared/IDL:IceSess\\\\/SessMgr:1\\\\.0.IDL/Common/!ICESMS\\\\/RESB!ICESMSLB\\\\/RES.LB!-2955511136615197053!533177!0"
