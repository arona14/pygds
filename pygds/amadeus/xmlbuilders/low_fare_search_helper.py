from pygds.core.types import FareOptions, TravelFlightInfo
from pygds.core.request import RequestedSegment
from typing import List


def generate_number_of_unit(traveling_number, number_of_unit_rc):

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


def generate_pax_reference(traveling_number):

    content = ""
    if traveling_number.adults:
        content += f"""
            <paxReference>
                <ptc>ADT</ptc>
                {"".join([f"<traveller><ref>{index +1}</ref></traveller>" for index in range(traveling_number.adults)])}
            </paxReference>
        """

    if traveling_number.children:
        content += f"""
            <paxReference>
                <ptc>CH</ptc>
                {"".join([f"<traveller><ref>{traveling_number.adults + index +1}</ref></traveller>" for index in range(traveling_number.children)])}
            </paxReference>
        """

    if traveling_number.infants:
        content += f"""
            <paxReference>
                <ptc>INF</ptc>
                {"".join([f"<traveller><ref>{index +1}</ref><infantIndicator>1</infantIndicator></traveller>" for index in range(traveling_number.infants)])}
            </paxReference>
        """

    return content


def generate_fare_options(fare_options: FareOptions):

    pricing_tick_info = ""

    if fare_options.price_type_rp:
        pricing_tick_info += "<priceType>RP</priceType>"
    if fare_options.price_type_ru:
        pricing_tick_info += "<priceType>RU</priceType>"
    if fare_options.price_type_et:
        pricing_tick_info += "<priceType>ET</priceType>"
    if fare_options.price_type_tac:
        pricing_tick_info += "<priceType>TAC</priceType>"
    if fare_options.price_type_cuc:
        pricing_tick_info += "<priceType>CUC</priceType>"

    conversion_rate = ""

    if fare_options.currency_usd:
        conversion_rate += "<currency>USD</currency>"
    else:
        conversion_rate += "<currency>USD</currency>"

    return f"""<fareOptions>
                        <pricingTickInfo>
                            <pricingTicketing>
                                {pricing_tick_info}
                            </pricingTicketing>
                        </pricingTickInfo>
                        <conversionRate>
                            <conversionRateDetail>
                                {conversion_rate}
                            </conversionRateDetail>
                        </conversionRate>
                    </fareOptions>"""


def generate_travel_flight_info(travel_flight_info: TravelFlightInfo):
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
