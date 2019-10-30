from typing import List

from pygds.amadeus.price import InformativeFareTax
from pygds.core.payment import CreditCard, FormOfPayment
from pygds.core.price import PriceRequest
from pygds.core.types import TravellerNumbering, Itinerary, FlightSegment
from pygds.core.request import RequestedSegment, LowFareSearchRequest


def mptbs_itinerary(segment: RequestedSegment):
    # origin = segment.departure.airport if segment.departure.airport is not None else segment.departure.city
    # destination = segment.arrival.airport if segment.arrival.airport is not None else segment.arrival.city
    # departure_date = segment.departure.date
    origin = segment.origin
    destination = segment.destination
    departure_date = segment.departure_date
    return f"""
    <itinerary>
        <requestedSegmentRef>
            <segRef>{segment.sequence}</segRef>
        </requestedSegmentRef>
        <departureLocalization>
            <depMultiCity>
                <locationId>{origin}</locationId>
                <airportCityQualifier>C</airportCityQualifier>
            </depMultiCity>
        </departureLocalization>
        <arrivalLocalization>
            <arrivalMultiCity>
                <locationId>{destination}</locationId>
                <airportCityQualifier>C</airportCityQualifier>
            </arrivalMultiCity>
        </arrivalLocalization>
        <timeDetails>
            <firstDateTimeDetail>
                <date>{departure_date}</date>
            </firstDateTimeDetail>
            <rangeOfDate>
                <rangeQualifier>M</rangeQualifier>
                <dayInterval>2</dayInterval>
            </rangeOfDate>
        </timeDetails>
    </itinerary>
    """


def mptbs_price_to_beat(price: float):
    return f"""
    <priceToBeat>
        <moneyInfo>
            <amount>{price}</amount>
        </moneyInfo>
    </priceToBeat>
    """


def mptbs_currency_conversion(currency: str):
    """
        Must be in <fareOptions>. And CUC must be specified in priceType
        <fareOptions>
            <pricingTickInfo>
                <pricingTicketing>
                    <priceType>CUC</priceType>
    """
    if currency is None:
        return ''
    return f"""
    <conversionRate>
        <conversionRateDetail>
            <currency>{currency}</currency>
        </conversionRateDetail>
    </conversionRate>
    """


def mptbs_pricing_types_com(types: str = None, identify: str = ""):
    return f"""
    <corporate>
        <corporateId>
            <corporateQualifier>{types}</corporateQualifier>
            <identity>{identify}</identity>
        </corporateId>
        </corporate>
    """


def mptbs_pricing_types(types: List[str]):
    price_types = "\n".join([f"<priceType>{p_type}</priceType>" for p_type in types])
    return f"""
    <pricingTicketing>
        {price_types}
    </pricingTicketing>
    """


def mptbs_exclude_point(point: str):
    """ Must be in <flightInfo> """
    return f"""
    <exclusionDetail>
        <exclusionIdentifier>X</exclusionIdentifier>
        <locationId>{point}</locationId>
    </exclusionDetail>
    """


def mptbs_include_point(point: str):
    """ Must be in <flightInfo> """
    return f"""
     <inclusionDetail>
        <inclusionIdentifier>M</inclusionIdentifier>
        <locationId>{point}</locationId>
    </inclusionDetail>
    """


def sell_from_recommendation_itinerary_details(origin, destination, segments):
    segments_part = ""
    for s in segments:
        segments_part += sell_from_recommendation_segment(s.origin, s.destination, s.departure_date, s.company,
                                                          s.flight_number, s.booking_class, s.quantity)
    return f"""
        <itineraryDetails>
            <originDestinationDetails>
                <origin>{origin}</origin>
                <destination>{destination}</destination>
            </originDestinationDetails>
            <message>
                <messageFunctionDetails>
                    <messageFunction>183</messageFunction>
                </messageFunctionDetails>
            </message>
            {segments_part}
        </itineraryDetails>
        """


def sell_from_recommendation_segment(origin, destination, departure_date, company, flight_number,
                                     booking_class, quantity):
    return f"""
    <segmentInformation>
        <travelProductInformation>
            <flightDate>
                <departureDate>{departure_date}</departureDate>
            </flightDate>
            <boardPointDetails>
                <trueLocationId>{origin}</trueLocationId>
            </boardPointDetails>
            <offpointDetails>
                <trueLocationId>{destination}</trueLocationId>
            </offpointDetails>
            <companyDetails>
                <marketingCompany>{company}</marketingCompany>
            </companyDetails>
            <flightIdentification>
                <flightNumber>{flight_number}</flightNumber>
                <bookingClass>{booking_class}</bookingClass>
            </flightIdentification>
        </travelProductInformation>
        <relatedproductInformation>
            <quantity>{quantity}</quantity>
            <statusCode>NN</statusCode>
        </relatedproductInformation>
    </segmentInformation>
    """


def add_multi_elements_traveller_info(ref_number, first_name, surname, last_name, date_of_birth, pax_type,
                                      infant_name=None):
    quantity = 1
    infant_part = ""
    infant_indicator = ""
    if infant_name is not None:
        quantity = 2
        infant_part = f"""
        <passenger>
            <firstName>{infant_name}</firstName>
            <type>INF</type>
        </passenger>
        """
        infant_indicator = "<infantIndicator>2</infantIndicator>"

    return f"""
        <travellerInfo>
            <elementManagementPassenger>
                <reference>
                    <qualifier>PR</qualifier>
                    <number>{ref_number}</number>
                </reference>
                <segmentName>NM</segmentName>
            </elementManagementPassenger>
            <passengerData>
                <travellerInformation>
                    <traveller>
                        <surname>{surname}</surname>
                        <quantity>{quantity}</quantity>
                    </traveller>
                    <passenger>
                        <firstName>{first_name}</firstName>
                        <type>{pax_type}</type>
                        {infant_indicator}
                    </passenger>
                    {infant_part}
                </travellerInformation>
            <dateOfBirth>
                <dateAndTimeDetails>
                    <date>{date_of_birth}</date>
                </dateAndTimeDetails>
            </dateOfBirth>
            </passengerData>
        </travellerInfo>
        """


def generate_seat_traveller_numbering(traveller_numbering: TravellerNumbering):
    adults = ""
    children = ""
    infants = ""
    if traveller_numbering.adults != 0:
        adults = _traveler_ref("ADT", 1, traveller_numbering.adults)
    if traveller_numbering.children != 0:
        children = _traveler_ref("CH", traveller_numbering.adults + 1, traveller_numbering.children)
    if traveller_numbering.infants != 0:
        infants = _traveler_ref("INF", 1, traveller_numbering.infants)
    return f"""
        {adults}
        {children}
        {infants}
        """


def _traveler_ref(pax_type, begin, pax_number):
    travellers = ""
    infant_indicator = ""
    if pax_type == 'INF':
        infant_indicator = "<infantIndicator>1</infantIndicator>"
    for ref in range(begin, begin + pax_number):
        travellers += f"""
            <traveller>
                <ref>{ref}</ref>
                {infant_indicator}
            </traveller>
            """
    return f"""
        <paxReference>
            <ptc>{pax_type}</ptc>
            {travellers}
        </paxReference>

        """


def travel_flight_info(low_fare_search: LowFareSearchRequest, c_qualifier=None):
    c_qualifier = "<cabinQualifier>RC</cabinQualifier>"
    return f"""
        <travelFlightInfo>
            <cabinId>
                {c_qualifier}
                <cabin>{low_fare_search.csv}</cabin>
            </cabinId>
            {_tfi_company_identity(low_fare_search.preferredAirlines)}
        </travelFlightInfo>
        """


def _tfi_company_identity(carrier_ids: List[str] = ""):
    carrier_qualifier = "<carrierQualifier>F</carrierQualifier>"
    carrierid_flightinfo = "\n".join([f"<carrierId>{carrierid}</carrierId>" for carrierid in carrier_ids])
    return f"""
    <companyIdentity>
        {carrier_qualifier}
        {carrierid_flightinfo}
    </companyIdentity>
    """


def add_multi_element_data_element(segment_name, qualifier, data_type, free_text):
    if free_text is None:
        return ""
    return f"""
        <dataElementsIndiv>
            <elementManagementData>
                <segmentName>{segment_name}</segmentName>
            </elementManagementData>
            <freetextData>
                <freetextDetail>
                    <subjectQualifier>{qualifier}</subjectQualifier>
                    <type>{data_type}</type>
                </freetextDetail>
                <longFreetext>{free_text}</longFreetext>
            </freetextData>
        </dataElementsIndiv>
    """


def add_multi_element_contact_element(contact_type, contact):
    return add_multi_element_data_element("AP", "3", contact_type, contact)


def fare_informative_price_passengers(travellers_info: TravellerNumbering):
    """
    Fare_InformativePricingWihtoutPNR
    :param travellers_info:
    :return:
    """
    group_number = 1
    adults, children, infants = "", "", ""
    start = 1
    if travellers_info.adults > 0:
        adults = _fare_informative_price_passenger_group(group_number, start, travellers_info.adults, 'ADT')
        start = travellers_info.adults
        group_number += 1
    if travellers_info.children > 0:
        children = _fare_informative_price_passenger_group(group_number, start, travellers_info.children, 'CH')
        group_number += 1
    if travellers_info.infants > 0:
        infants = _fare_informative_price_passenger_group(group_number, 1, travellers_info.infants, 'INF')
    return f"""
    {adults}
    {children}
    {infants}
    """


def fare_informative_price_segments(itineraries: List[Itinerary]):
    result = ""
    segment_idx = 1
    itinerary_idx = 1
    for itinerary in itineraries:
        segments = ""
        for segment in itinerary.segments:
            segments += _fare_informative_price_segment(segment, itinerary_idx, segment_idx)
            segment_idx += 1
        result += f"""
        <segmentGroup>
            {segments}
        </segmentGroup>
        """
        itinerary_idx += 1
    return result


def _fare_informative_price_segment(segment: FlightSegment, itinerary_no: int, segment_global_no: int):
    return f"""
    <segmentInformation>
       <flightDate>
            <departureDate>{segment.departure_date_time}</departureDate>
        </flightDate>
        <boardPointDetails>
            <trueLocationId>{segment.departure_airport}</trueLocationId>
        </boardPointDetails>
        <offpointDetails>
            <trueLocationId>{segment.arrival_airpot}</trueLocationId>
        </offpointDetails>
        <companyDetails>
            <marketingCompany>{segment.marketing}</marketingCompany>
        </companyDetails>
        <flightIdentification>
            <flightNumber>{segment.flight_number}</flightNumber>
            <bookingClass>{segment.class_of_service}</bookingClass>
        </flightIdentification>
        <flightTypeDetails>
            <flightIndicator>{itinerary_no}</flightIndicator>
        </flightTypeDetails>
        <itemNumber>{segment_global_no}</itemNumber>
    </segmentInformation>
    """


def _fare_informative_price_passenger_group(sequence_no, start, count, pax_type):
    if count is None or count == 0:
        return ""
    travellers = ""
    for i in range(start, count + start):
        travellers += f"""
        <travellerDetails>
              <measurementValue>{i}</measurementValue>
       </travellerDetails>
        """
    infant_indicator = ""
    if pax_type == "INF":
        infant_indicator = """
        <fareDetails>
          <qualifier>766</qualifier>
        </fareDetails>
        """
    return f"""
    <passengersGroup>
        <segmentRepetitionControl>
           <segmentControlDetails>
              <quantity>{sequence_no}</quantity>
              <numberOfUnits>{count}</numberOfUnits>
           </segmentControlDetails>
        </segmentRepetitionControl>
        <travellersID>
           {travellers}
        </travellersID>
        <discountPtc>
           <valueQualifier>{pax_type}</valueQualifier>
           {infant_indicator}
        </discountPtc>
     </passengersGroup>
    """


def ppwbc_passenger_segment_selection(price_request: PriceRequest):
    if not price_request or not (price_request.segments or price_request.passengers):
        return ""
    pax_refs = []
    seg_refs = []
    for r in price_request.passengers:
        pax_refs.append(_ppwbc_ref_detail("P", r))
    for s in price_request.segments:
        seg_refs.append(_ppwbc_ref_detail("S", s))
    return f"""
    <pricingOptionGroup>
        <pricingOptionKey>
            <pricingOptionKey>SEL</pricingOptionKey>
        </pricingOptionKey>
        <paxSegTstReference>
            {"".join(pax_refs)}
            {"".join(seg_refs)}
        </paxSegTstReference>
    </pricingOptionGroup>
    """


def _ppwbc_ref_detail(ref_type, ref_value):
    """
    This method generates price reference details for Price Pnr With Booking Class
    :param ref_type: The reference type (P for Passenger, S for Segment, PA, PI)
    :param ref_value: The value of the reference
    :return: an XML portion
    """
    return f"""
    <referenceDetails>
        <type>{ref_type}</type>
        <value>{ref_value}</value>
    </referenceDetails>"""


_fare_types_association = {
    "PUB": "RP",
    "NET": "RU",
    "COM": "RC"
}


def ppwbc_fare_type(fare_type):
    try:
        code = _fare_types_association[fare_type]
    except KeyError:
        return ""
    return f"""<pricingOptionGroup>
                    <pricingOptionKey>
                        <pricingOptionKey>{code}</pricingOptionKey>
                    </pricingOptionKey>
                </pricingOptionGroup>
                """


def ppwbc_discount():
    return """
    <discountInformation>
        <penDisInformation>
          <infoQualifier>ZAP</infoQualifier>
          <penDisData>
            <penaltyType>701</penaltyType>
            <penaltyQualifier>708</penaltyQualifier>
            <penaltyAmount>10</penaltyAmount>
            <discountCode>AC479</discountCode>
          </penDisData>
        </penDisInformation>
    </discountInformation>
    """


def ticket_issue_tst_ref(ref):
    return f"""
    <referenceDetails>
        <type>TS</type>
        <value>{ref}</value>
    </referenceDetails>"""


def issue_ticket_pax(ref_type, ref):
    return f"""
    <paxSelection>
        <passengerReference>
            <type>{ref_type}</type>
            <value>{ref}</value>
        </passengerReference>
    </paxSelection>
    """


def queue_place_target_queue(pcc: str, queue_number: str, category: str = "0"):
    return f"""
    <targetDetails>
        <targetOffice>
            <sourceType>
                <sourceQualifier1>3</sourceQualifier1>
            </sourceType>
            <originatorDetails>
                <inHouseIdentification1>{pcc}</inHouseIdentification1>
            </originatorDetails>
        </targetOffice>
        <queueNumber>
            <queueDetails>
                <number>{queue_number}</number>
            </queueDetails>
        </queueNumber>
        <categoryDetails>
            <subQueueInfoDetails>
                <identificationType>C</identificationType>
                <itemNumber>{category}</itemNumber>
            </subQueueInfoDetails>
        </categoryDetails>
    </targetDetails>
    """


def fibpwp_pax_groups(numbering: TravellerNumbering):
    """
    Fare_InformativeBestPricingWithoutPNR
    :param numbering: TravellerNumbering -> The object holding info about travellers
    :return: str
    """
    return fare_informative_price_passengers(numbering)


def fibpwp_add_taxes(tax_infos: List[InformativeFareTax]):
    """
    builds pricing option group to add taxes (AT)
    :param tax_infos: List[InformativeFareTax]
    :return: str
    """
    f"""
    <pricingOptionGroup>
        <pricingOptionKey>
            <pricingOptionKey>AT</pricingOptionKey>
        </pricingOptionKey>
        {"".join([_fibpwp_tax(t) for t in tax_infos])}
    </pricingOptionGroup>
    """


def fibpwp_add_country_taxes(tax_infos: List[InformativeFareTax]):
    """
    builds pricing option group to add country taxes (AC)
    :param tax_infos: List[InformativeFareTax]
    :return: str
    """
    f"""
    <pricingOptionGroup>
        <pricingOptionKey>
            <pricingOptionKey>AC</pricingOptionKey>
        </pricingOptionKey>
        {"".join([_fibpwp_tax(t) for t in tax_infos])}
    </pricingOptionGroup>
    """


def _fibpwp_tax(tax_information: InformativeFareTax):
    """
    This method generate tax information block for Fare_InformativeBestPricingWithoutPNR
    :param tax_information: InformativeFareTax -> Holds tax infos
    :return: str
    """
    return f"""
    <taxInformation>
        <taxQualifier>7</taxQualifier>
        <taxType>
            <isoCountry>{tax_information.country}</isoCountry>
        </taxType>
        <taxNature>{tax_information.nature}</taxNature>
        <taxData>
            <taxRate>{tax_information.rate}</taxRate>
            <taxValueQualifier>{tax_information.value_type}</taxValueQualifier>
        </taxData>
    </taxInformation>
    """


def itc_pax_selection(passenger_tattoo: str):
    return f"""
    <paxSelection>
        <passengerReference>
            <type>PT</type>
            <value>{passenger_tattoo}</value>
        </passengerReference>
    </paxSelection>
    """


def itc_option_group(indicator: str):
    return f"""
    <optionGroup>
        <switches>
            <statusDetails>
                <indicator>{indicator}</indicator>
            </statusDetails>
        </switches>
    </optionGroup>
    """


def itc_segment_select(segments: List[str]):
    return f"""
    <selection>
        {"".join([_itc_single_segment_select(s) for s in segments])}
    </selection>
    """


def _itc_single_segment_select(segment_tattoo):
    return f"""
    <referenceDetails>
        <type>ST</type>
        <value>{segment_tattoo}</value>
    </referenceDetails>
    """


def tcd_ticket_number(ticket_number: str):
    return f"""
    <documentNumberDetails>
        <documentDetails>
            <number>{ticket_number}</number>
        </documentDetails>
    </documentNumberDetails>
    """


def fop_credit_card(credit_card: CreditCard):
    return f"""
    <creditCardData>
        <creditCardDetails>
            <ccInfo>
                <vendorCode>{credit_card.vendor_code}</vendorCode>
                <cardNumber>{credit_card.card_number}</cardNumber>
                <securityId>{credit_card.security_id}</securityId>
                <expiryDate>{credit_card.expiry_date}</expiryDate>
            </ccInfo>
        </creditCardDetails>
    </creditCardData>
    """


def fop_form_of_payment(fop: FormOfPayment):
    if isinstance(fop, CreditCard):
        return fop_credit_card(fop)
    return f"""
    """


def fop_passenger(passenger_type, passenger_value):
    return f"""
    <passengerAssociation>
        <passengerReference>
            <type>{passenger_type}</type>
            <value>{passenger_value}</value>
        </passengerReference>
    </passengerAssociation>
    """


def fop_tst():
    pass


def fop_segment(segment_ref):
    return f"""
    <pnrElementAssociation>
        <referenceDetails>
            <type>SEG</type>
            <value>{segment_ref}</value>
        </referenceDetails>
    </pnrElementAssociation>
    """


def fop_sequence_number(sequence_number: str):
    return f"""
    <fopSequenceNumber>
        <sequenceDetails>
            <number>{sequence_number}</number>
        </sequenceDetails>
    </fopSequenceNumber>
    """
