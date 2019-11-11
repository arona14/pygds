"""
    This is for testing purposes like a suite.
"""

from pygds.core.request import RequestedSegment, LowFareSearchRequest
from pygds.core.types import TravellerNumbering, FareOptions, TravelFlightInfo
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


itineraries = [
    RequestedSegment(
        sequence=1, origin=None, destination=None, departure_date=None, arrival_date=None, total_seats=None, airport_city_qualifier="C")]

traveller = TravellerNumbering(1)

travel_flight_info = TravelFlightInfo(cabin="Y",
                                      rules_cabin="RC",
                                      airlines=["DL", "AF"],
                                      rules_airline="F")
fare_options = FareOptions(price_type_et=True,
                           price_type_rp=True,
                           priceType_ru=True,
                           price_type_tac=True,
                           priceType_cuc=True,
                           currency_eur=True,
                           currency_usd=False)

low_fare_search = LowFareSearchRequest(
    itineraries, travelingNumber=traveller, fare_options=fare_options, travel_flight_info=travel_flight_info
)

search_results = client.fare_master_pricer_travel_board_search(low_fare_search)


ressults, session_info = (search_results.payload, search_results.session_info)
