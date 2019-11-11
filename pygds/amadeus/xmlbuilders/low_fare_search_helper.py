from pygds.core.types import FareOptions, TravelFlightInfo


def generate_number_of_unit(self, traveling_number, number_of_unit_rc):

    return f"""<numberOfUnit>
                <unitNumberDetail>
                    <numberOfUnits>{traveling_number.total_travellers()}</numberOfUnits>
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
                <ptc>ADT</ptc>
                {"".join([f"<traveller><ref>{index +1}</ref></traveller>" for index in range(traveling_number.children)])}
            </paxReference>
        """

    if traveling_number.infants:
        content += f"""
            <paxReference>
                <ptc>ADT</ptc>
                {"".join([f"<traveller><ref>{index +1}</ref></traveller>" for index in range(traveling_number.infants)])}
            </paxReference>
        """

    return content


def generate_fare_options(fare_options: FareOptions):

    pricing_tick_info = ""

    if fare_options.price_type_rp:
        pricing_tick_info += "<priceType>RP</priceType>"
    if fare_options.priceType_ru:
        pricing_tick_info += "<priceType>RU</priceType>"
    if fare_options.price_type_et:
        pricing_tick_info += "<priceType>ET</priceType>"
    if fare_options.price_type_tac:
        pricing_tick_info += "<priceType>TAC</priceType>"
    if fare_options.priceType_cuc:
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
