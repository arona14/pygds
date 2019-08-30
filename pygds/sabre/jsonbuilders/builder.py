from pygds.sabre.jsonbuilders.search_builder import BFMBuilder
from pygds.core.request import LowFareSearchRequest


class SabreJSONBuilder:
    """This class can generate JSON needed for sabre search flight requests."""

    def __init__(self, target):
        self.target = target

    def search_flight_builder(self, search_request: LowFareSearchRequest, available_flights_only: bool = True, types: str = "PUB"):
        search_request = BFMBuilder(search_request)
        return {
            "OTA_AirLowFareSearchRQ": {
                "POS": search_request.pos(),
                "OriginDestinationInformation": search_request.origin_destination_information(),
                "TravelPreferences": search_request.travel_preferences(),
                "TravelerInfoSummary": search_request.travel_info_summary(types),
                "TPA_Extensions": search_request.tpa_extensions(),
                "Target": self.target,
                "Version": "4.1.0",
                "AvailableFlightsOnly": available_flights_only
            }
        }
