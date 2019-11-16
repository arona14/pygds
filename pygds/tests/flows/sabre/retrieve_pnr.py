"""
    This is for testing purposes like a suite.
"""
from typing import List

from pygds.core.helpers import get_data_from_json_safe as from_json_safe, ensure_list
from pygds import log_handler
from pygds.core.security_utils import decode_base64
from pygds.core.types import Itinerary
from pygds.env_settings import get_setting
from pygds.sabre.client import SabreClient
import os

from pygds.sabre.json_parsers.revalidate_extract import RevalidateItinerarieInfo
from pygds.sabre.jsonbuilders.revalidate import FlightSegment, Itineraries


def test():
    """ A suite of tests """

    dir_path = os.path.dirname(os.path.realpath(__file__))
    dir_path = os.path.join(dir_path, "..", "..", "..", "..")
    os.makedirs(os.path.join(dir_path, "out"), exist_ok=True)
    log_handler.load_file_config(os.path.join(dir_path, "log_config.yml"))
    log = log_handler.get_logger("test_all")

    username = get_setting("SABRE_USERNAME")
    pcc = get_setting("SABRE_PCC")
    password = decode_base64(get_setting("SABRE_PASSWORD"))
    soap_url = "https://webservices3.sabre.com"
    rest_url = "https://api.havail.sabre.com"
    client = SabreClient(soap_url, rest_url, username, password, pcc, True)

    pnr = "LAGNCH"  # "SCUCUT", "LAGNCH", "TGZKPI"
    token = None

    try:
        log.info(f"1.------------------ Retrieve PNR {pnr}--------------")
        retrieve_pnr = client.get_reservation(token, False, pnr)
        closed = retrieve_pnr.session_info.session_ended
        if closed is True:
            log.info("Session already closed")
            return
        if retrieve_pnr.application_error:
            log.error(f"Error when retrieving PNR: {retrieve_pnr.application_error.description}")
            return
        retrieve_pnr, token = retrieve_pnr.payload, retrieve_pnr.session_info.security_token
        log.debug(retrieve_pnr)
        if closed is False:
            client.close_session(token)
    except Exception as ex:
        log.exception(ex, exc_info=True)
        client.close_session(token)


if __name__ == "__main__":
    test()
