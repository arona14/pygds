from pygds.core.types import TravellerNumbering


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


def add_multi_elements_traveller_info(ref_number, first_name, surname, last_name, date_of_birth, pax_type):
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
                    <quantity>1</quantity>
                </traveller>
                <passenger>
                    <firstName>{first_name}</firstName>
                    <type>{pax_type}</type>
                </passenger>
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
