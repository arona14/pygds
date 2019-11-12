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
    client = SabreClient(soap_url, rest_url, username, password, pcc, False)

    pnr = "LAGNCH"  # "TGZKPI"
    second_pnr = "TGZKPI"
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

        log.info("2.------------------------------Search Price--------------")
        fare_type = "Pub"
        passenger_types_search = [{"name_select": [p.name_id], "code": p.passenger_type, "quantity": p.number_in_party} for p in retrieve_pnr["passengers"]]
        passenger_types_store = [{"name_select": p.name_id, "code": p.passenger_type, "quantity": p.number_in_party,
                                  "commission_percent": 10, "markup": 0, "tour_code": "FF", "ticket_designator": "ABC",
                                  "service_fee": 10} for p in retrieve_pnr["passengers"]]
        search_segment_ids = [s.sequence for it in retrieve_pnr["itineraries"] for s in it.segments]
        log.debug(f"Name ids: {passenger_types_search}")
        log.debug(f"Segment ids: {search_segment_ids}")
        search_result = client.search_price_quote(token, False, fare_type, search_segment_ids, passenger_types_search, 0, "")

        closed = search_result.session_info.session_ended
        if closed is True:
            log.info("Session already closed")
            return
        if search_result.application_error:
            log.error(f"Error when searching price: {search_result.application_error.description}")
            return
        search_result, token = search_result.payload, search_result.session_info.security_token
        log.debug(search_result)

        log.info("3.--------------------------- Revalidate itineraries ---------------")
        itineraries: List[Itinerary] = None
        itineraries, segment_map = get_itineraries_pnr(retrieve_pnr["itineraries"])
        # segment_map = {i: {} for i, it in enumerate(itineraries)}
        revalidate_result = client.revalidate_itinerary(itineraries, passenger_types_search, fare_type)

        if revalidate_result.application_error:
            log.error(f"Error when re-validating itineraries: {revalidate_result.application_error.description}")
            return
        revalidate_info: RevalidateItinerarieInfo = revalidate_result.payload
        log.debug(revalidate_info)
        brand_segments = {}
        log.debug(f"type of revalidate_result: {type(revalidate_info)}")
        priced_itineraries = from_json_safe(revalidate_info.priced_itinerarie, "PricedItinerary")
        for priced_itineray in ensure_list(priced_itineraries):
            additional_fares = from_json_safe(priced_itineray, "TPA_Extensions", "AdditionalFares")
            for additional_fare in ensure_list(additional_fares):
                ptc_breakdowns = from_json_safe(additional_fare, "AirItineraryPricingInfo", "PTC_FareBreakdowns", "PTC_FareBreakdown")
                for ptc_breakdown in ensure_list(ptc_breakdowns):
                    passenger_fare = from_json_safe(ptc_breakdown, "PassengerFare")
                    # log.debug(passenger_fare)
                    fare_components = from_json_safe(passenger_fare, "TPA_Extensions", "FareComponents", "FareComponent")
                    # log.debug(f"fare_components: {fare_components}")
                    brands = []
                    for brand in ensure_list(fare_components):
                        brand_id = from_json_safe(brand, "BrandID")
                        applicable_segments = []
                        for s in ensure_list(from_json_safe(brand, "Segment")):
                            itin_index = from_json_safe(s, "LegIndex")
                            segment_idex = from_json_safe(s, "FlightIndex")
                            segment_id = get_segment_id(segment_map, itin_index, segment_idex)
                            applicable_segments.append(segment_id)
                            update_segment_brands(brand_segments, segment_id, brand_id)
                        brands.append({"brand_id": brand_id, "applicable_segments": applicable_segments})
                    log.debug(brands)
        # PricedItineraries
        # PricedItinerary list[0]
        # TPA_Extensions
        # AdditionalFares list
        # AirItineraryPricingInfo
        # PTC_FareBreakdowns
        # PTC_FareBreakdown list
        # PassengerFare
        # TPA_Extensions
        # FareComponents
        # FareComponent list

        log.debug("4.-------------------- Store Price ---------------------")
        # store_segment_ids = [(i, get_first_brand(brand_segments, i)) for i in search_segment_ids]
        store_segment_ids = [(i, None) for i in search_segment_ids]
        # store_segment_ids = [(i, "D2") for i in search_segment_ids]
        for p in passenger_types_store:
            log.info(f"Store for passenger {p['name_select']}")
            store_result = client.store_price_quote(token, False, fare_type, store_segment_ids, p, 0, "", None)

            closed = store_result.session_info.session_ended
            if closed is True:
                log.info("Session already closed")
                return
            if store_result.application_error:
                log.error(f"Error when storing price: {store_result.application_error.description}")
                client.close_session(token)
                return
            store_result, token = store_result.payload, store_result.session_info.security_token
            # log.debug(store_result)
        # log.info(f"------------------ Retrieve PNR {second_pnr}--------------")
        # token = retrieve_pnr.session_info.security_token
        # retrieve_pnr = client.get_reservation(token, True, second_pnr)
        # log.debug(retrieve_pnr)
        # closed = retrieve_pnr.session_info.session_ended
        if closed is False:
            client.close_session(token)
    except Exception as ex:
        log.exception(ex, exc_info=True)
        client.close_session(token)


def update_segment_brands(brand_segments: dict, segment_id: int, brand_id: str):
    try:
        segment_brands = brand_segments[segment_id]
    except KeyError:
        segment_brands = []
        brand_segments[segment_id] = segment_brands
    segment_brands.append(brand_id)
    return segment_brands


def get_first_brand(brand_segments: dict, segment_id: int) -> str:
    try:
        return brand_segments[segment_id][-1]
    except (KeyError, IndexError):
        return None


def get_itineraries_pnr(itineraries: List[Itinerary]):
    """[lists of segments of a given pnr]

    Arguments:
    itineraries:
    Returns:
        [list] -- [description]
    """
    list_itineraries = []
    seg_global_index = 1
    itin_indexes = {}

    for itin_index, itin in enumerate(itineraries):
        list_segments = []
        seg_indexes = {}
        for seg_index, seg in enumerate(itin.segments):
            flight = FlightSegment()
            flight.flight_number = int(seg.flight_number)
            flight.departure_date_time = seg.departure_date_time
            flight.arrival_date_time = seg.arrival_date_time
            flight.res_book_desig_code = seg.res_book_desig_code
            flight.origin_location = seg.departure_airport.airport
            flight.destination_location = seg.arrival_airport.airport
            flight.marketing_airline = seg.marketing.airline_code
            flight.operating_airline = seg.operating.airline_code
            list_segments.append(flight.to_dict())
            seg_indexes[seg_index + 1] = seg_global_index
            seg_global_index += 1
        itin_indexes[itin_index + 1] = seg_indexes
        origin = itin.segments[0].departure_airport.airport
        destination = itin.segments[-1].arrival_airport.airport
        departure_date = itin.segments[0].departure_date_time
        itinerary = Itineraries(str(itin_index + 1), origin, destination, departure_date, list_segments).to_dict()
        list_itineraries.append(itinerary)

    return list_itineraries, itin_indexes


def get_segment_id(segment_map, itin_index: int, segment_index: int):
    itin = segment_map[itin_index]
    return itin[segment_index]


if __name__ == "__main__":
    test()
