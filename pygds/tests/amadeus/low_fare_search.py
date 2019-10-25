"""
    This is for testing purposes like a suite.
"""

from pygds.core.request import RequestedSegment, LowFareSearchRequest
from pygds.core.types import TravellerNumbering
from pygds import log_handler
from pygds.env_settings import get_setting
import os
from pygds.amadeus.client import AmadeusClient
endpoint = get_setting("AMADEUS_ENDPOINT_URL")
username = get_setting("AMADEUS_USERNAME")
password = get_setting("AMADEUS_PASSWORD")
office_id = get_setting("AMADEUS_OFFICE_ID")
wsap = get_setting("AMADEUS_WSAP")
dir_path = os.path.dirname(os.path.realpath(__file__))
dir_path = os.path.join(dir_path, "..", "..", "..")
os.makedirs(os.path.join(dir_path, "out"), exist_ok=True)
log_handler.load_file_config(os.path.join(dir_path, "log_config.yml"))
log = log_handler.get_logger("test_all")
client = AmadeusClient(endpoint, username, password, office_id, wsap, False)


def low_fare_search(origin: str, destination: str, date_dep: str, date_arr: str):
    log.debug(f"make search in origin '{origin}' to the destination '{destination}'")
    segments = [RequestedSegment(origin=origin, destination=destination, departure_date=date_dep, arrival_date=date_arr)]
    low_fare_search = LowFareSearchRequest(segments, "Y", "", TravellerNumbering(1), "", "", ["DL", "AF"], "", "", 1)
    log.debug(f"making search from '{origin}' to '{destination}', starting at '{date_dep}' and arriving at '{date_arr}'")
    currency_code, c_qualifier = ("EUR", "RC")
    search_results = client.fare_master_pricer_travel_board_search(low_fare_search, currency_code, c_qualifier)
    log.debug("fare_master_pricer_travel_board_search")
    ressults, session_info = (search_results.payload, search_results.session_info)
    if session_info.session_ended:
        log.error("Session is ended after search")
        return
    log.debug(ressults)
