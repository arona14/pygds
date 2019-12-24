from pygds.core.types import FareOptions, TravelFlightInfo, TravellerNumbering
from pygds.core.request import RequestedSegment
from typing import List


def generate_number_of_unit(traveling_number: TravellerNumbering, number_of_unit_rc: int):
    """Generate xml content for number of unit in low fare search

    Arguments:
        traveling_number {TravellerNumbering} -- [Information of passenger]
        number_of_unit_rc {int} -- [number of passenger]

    Returns:
        [str] -- [xml content]
    """
    return f"""<numberOfUnit>
                <unitNumberDetail>
                    <numberOfUnits>{traveling_number.total_seats()}</numberOfUnits>
                    <typeOfUnit>PX</typeOfUnit>
                </unitNumberDetail>
                <unitNumberDetail>
                    <numberOfUnits>{number_of_unit_rc}</numberOfUnits>
                    <typeOfUnit>RC</typeOfUnit>
                </unitNumberDetail>
            </numberOfUnit>
        """


def get_pax_info(pax_type: str, number_passenger: int):
    """[summary]

    Arguments:
        pax_type {str} -- [passenger type]
        number_passenger {int} -- [number in party]

    Returns:
        [str] -- [xml content]
    """
    return f"""
            <paxReference>
                <ptc>{pax_type}</ptc>{"".join([f"<traveller><ref>{index +1}</ref></traveller>" for index in range(number_passenger)])}
            </paxReference>
        """


def generate_pax_reference(traveling_number: TravellerNumbering):
    """[generate xml content for passenger low fare search]

    Arguments:
        traveling_number {TravellerNumbering} -- [information passenger]

    Returns:
        [str] -- [content xml]
    """
    content = ""
    if traveling_number.adults:
        content += get_pax_info("ADT", traveling_number.adults)

    if traveling_number.children:
        content += get_pax_info("CH", traveling_number.children)

    if traveling_number.infants:
        content += get_pax_info("INF", traveling_number.infants)

    return content


def get_pricing_type(type: str):
    """generate pricing type

    Arguments:
        type {str} -- [pricing type]
    """
    return f"<priceType>{type}</priceType>"


def generate_fare_options(fare_options: FareOptions):
    """Generate xml content for fare type in low fare search

    Arguments:
        fare_options {FareOptions} -- [Content fare type option]

    Returns:
        [str] -- [content xml]
    """
    pricing_tick_info = ""

    if fare_options.price_type_rp:
        pricing_tick_info += get_pricing_type("RP")
    if fare_options.price_type_ru:
        pricing_tick_info += get_pricing_type("RU")
    if fare_options.price_type_et:
        pricing_tick_info += get_pricing_type("ET")
    if fare_options.price_type_tac:
        pricing_tick_info += get_pricing_type("TAC")
    if fare_options.price_type_cuc:
        pricing_tick_info += get_pricing_type("CUC")

    conversion_rate = ""

    if fare_options.currency_usd:
        conversion_rate += "USD"
    else:
        conversion_rate += "EUR"

    return f"""<fareOptions>
                        <pricingTickInfo>
                            <pricingTicketing>
                                {pricing_tick_info}
                            </pricingTicketing>
                        </pricingTickInfo>
                        <conversionRate>
                            <conversionRateDetail>
                                <currency>{conversion_rate}</currency>
                            </conversionRateDetail>
                        </conversionRate>
                    </fareOptions>"""


def generate_travel_flight_info(travel_flight_info: TravelFlightInfo):
    """Generate xml content for flight info in low fare search

    Arguments:
        travel_flight_info {TravelFlightInfo} -- [Information flight]

    Returns:
        [str] -- [xml content]
    """
    return f"""<travelFlightInfo>
                <cabinId>
                    <cabinQualifier>{travel_flight_info.rules_cabin}</cabinQualifier>
                    <cabin>{travel_flight_info.cabin}</cabin>
                </cabinId>
                <companyIdentity>
                    <carrierQualifier>{travel_flight_info.rules_airline}</carrierQualifier>
                    {"".join(["<carrierId>DL</carrierId>" for rules in travel_flight_info.rules_airline])}
                </companyIdentity>
            </travelFlightInfo>"""


def generate_itinerary(itineraries: List[RequestedSegment]):
    """
    This method is to generate a list of itinerary
    :param  itineraries: the  itineraries
    :return list of itineraries
    """

    content = ""
    for itinerary in itineraries:
        content += f"""<itinerary>
                        <requestedSegmentRef>
                            <segRef>{itinerary.sequence}</segRef>
                        </requestedSegmentRef>
                        <departureLocalization>
                            <depMultiCity>
                                <locationId>{itinerary.origin}</locationId>
                                <airportCityQualifier>{itinerary.airport_city_qualifier}</airportCityQualifier>
                            </depMultiCity>
                        </departureLocalization>
                        <arrivalLocalization>
                            <arrivalMultiCity>
                                <locationId>{itinerary.destination}</locationId>
                                <airportCityQualifier>{itinerary.airport_city_qualifier}</airportCityQualifier>
                            </arrivalMultiCity>
                        </arrivalLocalization>
                        <timeDetails>
                            <firstDateTimeDetail>
                                <date>{itinerary.departure_date}</date>
                            </firstDateTimeDetail>
                            <rangeOfDate>
                                <rangeQualifier>M</rangeQualifier>
                                <dayInterval>2</dayInterval>
                            </rangeOfDate>
                        </timeDetails>
                    </itinerary>"""
    return content
