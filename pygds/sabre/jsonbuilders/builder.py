import json
from .create_pnr import CreatePnrRequest

from pygds.sabre.jsonbuilders.search_builder import BFMBuilder
from pygds.core.request import LowFareSearchRequest

from pygds.sabre.jsonbuilders.create_pnr_builder import CreatePnrBuilder
from pygds.sabre.jsonbuilders.revalidate_builder import RevalidateBuilder


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

    def create_pnr_builder(self, create_pnr_request: CreatePnrRequest):

        create_builder = CreatePnrBuilder(create_pnr_request)
        return json.dumps(create_builder.to_dict(), sort_keys=False, indent=4)

    def revalidate_build(self, pcc, itineraries: list = [], passengers: list = [], fare_type: str = "Pub"):
        revalidate_builder = RevalidateBuilder(pcc, itineraries, passengers, fare_type, self.target)
        return {
            "OTA_AirLowFareSearchRQ": {
                "POS": revalidate_builder.pos(),
                "OriginDestinationInformation": revalidate_builder.origin_destination_information(),
                "TravelPreferences": revalidate_builder.travel_preference(),
                "TravelerInfoSummary": revalidate_builder.traveler_info_summary(),
                "Target": self.target,
                "Version": "4.3.0",
                "AvailableFlightsOnly": True
            }
        }
