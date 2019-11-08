from decimal import Decimal
from pygds.core.helpers import get_data_from_json_safe as from_json_safe

from pygds.core.types import FlightSegment, FlightPointDetails


def get_segment_number(segment_select):
    if segment_select != []:
        segment_number = "<ItineraryOptions>"
        for k in segment_select:
            segment_number = segment_number + "<SegmentSelect Number='" + str(k) + "'/>"
        segment_number = segment_number + "</ItineraryOptions>"
        return segment_number


def get_fare_type(fare_type):
    if fare_type == "Pub":
        return """<Account>
                    <Code>COM</Code>
                </Account>"""


def get_passenger_type(passenger_type, fare_type):

    child_list = ["CNN", "JNN", "J12", "J11", "J10", "J09", "J08", "J07", "J06", "J05", "J04", "J03", "J02", "C12", "C11", "C10", "C09", "C08", "C07", "C06", "C05", "C04", "C03", "C02"]
    pax_type = ""
    name_select = ""
    for pax in passenger_type:
        if fare_type == "Pub":
            pax_type = __get_pax_type_with_pub(pax, pax_type, child_list)
        elif fare_type == "Net":
            pax_type = __get_pax_type_with_net(pax, pax_type, child_list)
        for j in pax['name_select']:
            name_select = name_select + "<NameSelect NameNumber='" + str(j) + "'/>"
    return pax_type, name_select


def __get_pax_type_with_pub(pax, pax_type, child_list):
    if pax['code'] in ["ADT", "JCB"]:
        pax_type = pax_type + f"""<PassengerType Code="ADT" Quantity="{str(pax["quantity"])}"/>"""

    elif pax['code'] in child_list:
        code = "C" + str(pax['code'][-2:])
        pax_type = pax_type + "<PassengerType Code='" + code + "' Quantity='" + str(pax['quantity']) + "'/>"

    elif pax['code'] in ["INF", "JNF"]:
        pax_type = pax_type + f"""<PassengerType Code="INF" Quantity="{str(pax["quantity"])}"/>"""
    return pax_type


def __get_pax_type_with_net(pax, pax_type, child_list):
    if pax['code'] in ["ADT", "JCB"]:
        pax_type = pax_type + f"""<PassengerType Code="JCB" Quantity="{str(pax["quantity"])}"/>"""

    elif pax['code'] in child_list:
        code = "J" + str(pax['code'][-2:])
        pax_type = pax_type + "<PassengerType Code='" + code + "' Quantity='" + str(pax['quantity']) + "'/>"

    elif pax['code'] in ["INF", "JNF"]:
        pax_type = pax_type + f"""<PassengerType Code="JNF" Quantity="{str(pax["quantity"])}"/>"""
    return pax_type


hemisphere_code = {
    "United States": "0",
    "Central America": "1",
    "Caribbean": "2",
    "Latin America": "3",
    "Europe": "4",
    "Africa": "5",
    "Middle East": "6",
    "Asia ": "7",
    "Asia Pacific": "8",
    "Canada": "9"
}


def _get_hemisphere_code(region_name):
    return hemisphere_code.get(region_name, "0")


def get_commision(baggage, pcc, region_name):

    hemisphere_code = _get_hemisphere_code(region_name)
    commission = "<MiscQualifiers>"
    if baggage > 0:
        commission = commission + f"""<BaggageAllowance Number='{str(baggage)}'/>"""
    if pcc == "3GAH":
        commission = commission + f"""<HemisphereCode>{hemisphere_code}</HemisphereCode>
                                        <JourneyCode>'2'</JourneyCode>"""
    commission = commission + "</MiscQualifiers>"
    if commission == "<MiscQualifiers></MiscQualifiers>":
        commission = ""
    return commission


def __store_commission_with_pub(passenger_type_data, region_name, pcc):
    TWOPLACES = Decimal(10) ** -2
    hemisphere_code = _get_hemisphere_code(region_name)
    commission = ""
    if from_json_safe(passenger_type_data, 'commission_percent') > 0 and from_json_safe(passenger_type_data, 'tour_code') == "":
        commission_percentage = Decimal(passenger_type_data['commission_percent']).quantize(TWOPLACES)
        commission = commission + f"""<MiscQualifiers><Commission Percent='{str(commission_percentage)}'/>"""
        if pcc == "3GAH":
            commission = commission + f"""<HemisphereCode>{hemisphere_code}</HemisphereCode>
                                            <JourneyCode>'2'</JourneyCode>"""
        commission = commission + "</MiscQualifiers>"

    elif from_json_safe(passenger_type_data, 'commission_percent') > 0 and from_json_safe(passenger_type_data, 'tour_code') != "":
        commission_percentage = Decimal(passenger_type_data['commission_percent']).quantize(TWOPLACES)
        commission = commission + f"""<MiscQualifiers><Commission Percent='{str(commission_percentage)}'/>"""
        if pcc == "3GAH":
            commission = commission + f"""<HemisphereCode>{hemisphere_code}</HemisphereCode>"
                                            "<JourneyCode>'2'</JourneyCode>"""
        commission = commission + f"""<TourCode>
                <SuppressIT Ind='true'/>
                <Text>{passenger_type_data['tour_code']}</Text>
            </TourCode>
            </MiscQualifiers>"""
    return commission


def __store_commission_with_net(passenger_type_data, region_name, pcc):
    TWOPLACES = Decimal(10) ** -2
    commission = ""
    hemisphere_code = _get_hemisphere_code(region_name)
    if from_json_safe(passenger_type_data, 'markup') != "0" and pcc != "37AF":
        commission_amount = Decimal(passenger_type_data['markup']).quantize(TWOPLACES)
        commission = commission + f"""<MiscQualifiers><Commission Amount='{str(commission_amount)}'/>"""
        if pcc == "3GAH":
            commission = commission + f"""<HemisphereCode>{hemisphere_code}</HemisphereCode>
                                        <JourneyCode>'2'</JourneyCode>"""
        commission = commission + "</MiscQualifiers>"
    return commission


def store_commission(fare_type, passenger_type_data, region_name, pcc):
    commission = ""
    if fare_type == "Pub":
        commission = commission + __store_commission_with_pub(passenger_type_data, region_name, pcc)
    elif fare_type == "Net":
        commission = commission + __store_commission_with_net(passenger_type_data, region_name, pcc)

    if commission == "<MiscQualifiers></MiscQualifiers>":
        commission = ""
    return commission


def store_ticket_designator(passenger_type_data, segment_select, brand_id):
    ticket_designator = ""
    segment_number = ""

    if from_json_safe(passenger_type_data, 'ticket_designator') is not None and from_json_safe(passenger_type_data, 'ticket_designator') != "":
        segment_number = segment_number + "<ItineraryOptions>"
        for s in segment_select:
            segment_number = segment_number + f"""<SegmentSelect Number="{s}" RPH="1"/>"""
        segment_number = segment_number + "</ItineraryOptions>"

        ticket_designator = ticket_designator + f"""<CommandPricing RPH="1">
                                                        <Discount Percent='0' AuthCode='{passenger_type_data['ticket_designator']}'/>
                                                    </CommandPricing>"""
    elif brand_id is not None and brand_id != "":
        segment_number = segment_number + "<ItineraryOptions>"
        for s in segment_select:
            segment_number = segment_number + f"""<SegmentSelect Number="{s}" RPH="1"/>"""
        segment_number = segment_number + "</ItineraryOptions>"

        ticket_designator = f"""<Brand RPH="1">{brand_id}</Brand>"""
    else:
        segment_number = segment_number + "<ItineraryOptions>"
        for s in segment_select:
            segment_number = segment_number + f"""<SegmentSelect Number="{s}"/>"""
        segment_number = segment_number + "</ItineraryOptions>"

    return ticket_designator, segment_number


def store_pax_type(passenger_type_data):
    return f"""<PassengerType Code='{passenger_type_data['code']}' Quantity='1'/>"""


def store_name_select(passenger_type_data):
    return f"""<NameSelect NameNumber='{passenger_type_data['name_select']}'/>"""


def store_plus_up(passenger_type_data, pcc):
    TWOPLACES = Decimal(10) ** -2
    if from_json_safe(passenger_type_data, 'markup') > 0 and pcc != "37AF":
        commission_amount = Decimal(passenger_type_data['markup']).quantize(TWOPLACES)
        return f"""<PlusUp Amount='{str(commission_amount)}'></PlusUp>"""


def _add_flight_segment_to_air_book(segment):

    return f"""<FlightSegment DepartureDateTime="{segment.departure_date_time}"  ArrivalDateTime="{segment.arrival_date_time}" FlightNumber="{segment.flight_number}" NumberInParty="{segment.number_in_party}" ResBookDesigCode="{segment.res_book_desig_code}" Status="{segment.status}" InstantPurchase="false">
            <DestinationLocation LocationCode="{segment.arrival_airport.airport}"/>
            <MarketingAirline Code="{segment.marketing}" FlightNumber="{segment.flight_number}"/>
            <OperatingAirline Code="{segment.operating}"/>
            <OriginLocation LocationCode="{segment.departure_airport.airport}"/>
        </FlightSegment>"""


def add_flight_segments_to_air_book(segment_list):
    segments = ""
    for flight_segment in segment_list:
        arrival_airport = FlightPointDetails(airport=flight_segment['destination'])
        departure_airport = FlightPointDetails(airport=flight_segment['origin'])
        segment = FlightSegment(res_book_desig_code=flight_segment['res_book_desig_code'], departure_date_time=flight_segment['departure_date_time'], arrival_date_time=flight_segment['arrival_date_time'], flight_number=flight_segment['flight_number'], status=flight_segment['status'], arrival_airport=arrival_airport, departure_airport=departure_airport, marketing=flight_segment['marketing_code'], operating=flight_segment['operating_code'], number_in_party=flight_segment['number_in_party'])
        segments = segments + _add_flight_segment_to_air_book(segment)
    return segments


def exchange_pax(pnr, name_number, first_name, last_name, ticket_number):

    return f"""<PassengerWithPNR pnrLocator="{pnr}" referenceNumber="{name_number}" firstName="{first_name}" lastName="{last_name}">
                <DocumentNumber>{ticket_number}</DocumentNumber>
            </PassengerWithPNR>"""


def get_passengers_exchange(pnr, passengers):
    return "\n".join([exchange_pax(pnr, p["name_number"], p["first_name"], p["last_name"], p["ticket_number"]) for p in passengers])


def exchange_seg(departure_date_time, departure_airport, arrival_airport):

    return f"""<OriginDestinationInformation shopIndicator="true">
                <DateTimeSelection>
                    <DepartureDate>{departure_date_time}</DepartureDate>
                </DateTimeSelection>
                <StartLocation>{departure_airport}</StartLocation>
                <EndLocation>{arrival_airport}</EndLocation>
            </OriginDestinationInformation>"""


def get_segments_exchange(segments):
    return "\n".join([exchange_seg(s["departure_date_time"], s["departure_airport"], s["arrival_airport"]) for s in segments])


def get_form_of_payment(payment_type: str = None, code_card: str = None, expire_date: str = None, cc_number: str = None):

    if payment_type == "CC":
        return f"""<BasicFOP>
                        <CC_Info Suppress="true">
                            <PaymentCard Code="{code_card}" ExpireDate="{expire_date}" Number="{cc_number}"/>
                        </CC_Info>
                    </BasicFOP>"""
    else:
        return f"""<BasicFOP Type="{payment_type}"/>"""


def get_commission_exchange(fare_type, value):

    commission_value = ""
    if fare_type == "PUB" and value is not None and value > 0:
        commission_value = commission_value + f"""<MiscQualifiers><Commission Percent="{value}"/></MiscQualifiers>"""

    elif fare_type == "NET" and value is not None and value > 0:
        commission_value = commission_value + f"""<MiscQualifiers><Commission Amout="{value}"/></MiscQualifiers>"""

    return commission_value


def add_flight_segment(origin, destination, depart_date, operating_code, marketing_code, flight_number, arrival_date, class_of_service, currency_code):

    return f"""<tag0:Flight origin="{origin}" destination="{destination}">
      <tag0:DepartureDate>{depart_date}</tag0:DepartureDate>
      <tag0:Operating carrier="{operating_code}">{flight_number}</tag0:Operating>
      <tag0:Marketing carrier="{marketing_code}">{flight_number}</tag0:Marketing>
      <tag0:ArrivalDate>{arrival_date}</tag0:ArrivalDate>
    </tag0:Flight>
    <tag0:CabinDefinition>
      <tag0:RBD>{class_of_service}</tag0:RBD>
    </tag0:CabinDefinition>
    <Currency>{currency_code}</Currency>"""


def segments_to_cancel(segment_list):
    """[this function allows you to specify which segments to cancel]

    Arguments:
        segment_list {[list]} -- [description]
    """
    if len(segment_list) > 0:
        return "".join([f"""<Segment Number="{seg}"/>""" for seg in segment_list])
    elif len(segment_list) == 0 or segment_list is None:
        return """<Segment Type="air"/>"""
