def get_segment_number(segment_select):
    if segment_select != []:
        segment_number = "<ItineraryOptions>"
        for k in segment_select:
            segment_number = segment_number + "<SegmentSelect Number='" + str(k) + "'/>"
        segment_number = segment_number + "</ItineraryOptions>"
        return segment_number
    return None


def get_fare_type(fare_type):
    if fare_type == "Pub":
        fare_type_value = "<Account>"
        fare_type_value = fare_type_value + "<Code>COM</Code>"
        fare_type_value = fare_type_value + "</Account>"
        return fare_type_value
    return None


def get_passenger_type(passenger_type, fare_type):

    child_list = ["CNN", "JNN", "J12", "J11", "J10", "J09", "J08", "J07", "J06", "J05", "J04", "J03", "J02", "C12", "C11", "C10", "C09", "C08", "C07", "C06", "C05", "C04", "C03", "C02"]
    pax_type = ""
    name_select = ""
    for pax in passenger_type:
        if fare_type == "Pub":
            pax_type = __get_pax_type_with_pub(pax, pax_type, child_list)
        elif fare_type == "Net":
            pax_type = __get_pax_type_with_net(pax, pax_type, child_list)
        for j in pax['nameSelect']:
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


def _get_hemisphere_code(region_name):
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
    return hemisphere_code.get(region_name, "0")


def get_commision(baggage, pcc, region_name):

    hemisphere_code = _get_hemisphere_code(region_name)
    commission = "<MiscQualifiers>"
    if baggage > 0:
        commission = commission + "<BaggageAllowance Number='" + str(baggage) + "'/>"
    if pcc == "3GAH":
        commission = commission + "<HemisphereCode>" + hemisphere_code + "</HemisphereCode>"
        commission = commission + "<JourneyCode>" + '2' + "</JourneyCode>"

    commission = commission + "</MiscQualifiers>"
    if commission == "<MiscQualifiers></MiscQualifiers>":
        commission = ""
    return commission


def get_passengers_exchange(pnr, passengers):

    passenger_information = ""
    if passengers != []:
        for i in passengers:
            passenger_information = passenger_information + f"""<PassengerWithPNR pnrLocator="{pnr}" referenceNumber="{i["name_number"]}" firstName="{i["first_name"]}" lastName="{i["last_name"]}">
                <DocumentNumber>{i["ticketNumber"]}</DocumentNumber>
            </PassengerWithPNR>"""
    return passenger_information


def get_segments_exchange(segments):

    segment_information = ""
    if segments != []:
        for i in segments:
            segment_information = segment_information + f"""<OriginDestinationInformation shopIndicator="true">
            <DateTimeSelection>
                <DepartureDate>{i["departure_date_time"]}</DepartureDate>
            </DateTimeSelection>
            <StartLocation>{i["departure_airport"]}</StartLocation>
            <EndLocation>{i["arrival_airport"]}</EndLocation>
            </OriginDestinationInformation>"""
    return segment_information


def get_form_of_payment(data):

    if data["payment_type"] == "CC":
        payment_infos = f"""<BasicFOP>
                        <CC_Info Suppress="true">
                            <PaymentCard Code="{data["code_card"]}" ExpireDate="{data["expire_date"]}" Number="{data["cc_number"]}"/>
                        </CC_Info>
                    </BasicFOP>"""
        return payment_infos
    else:
        return f"""<BasicFOP Type="{data["payment_type"]}"/>"""


def get_commission_exchange(fare_type, commission_percentage, markup):

    commission_value = ""
    if fare_type == "PUB" and commission_percentage is not None and commission_percentage > 0:
        commission_value = commission_value + f"""<MiscQualifiers><Commission Percent="{commission_percentage}"/></MiscQualifiers>"""

    elif fare_type == "NET" and markup is not None and markup > 0:
        commission_value = commission_value + f"""<MiscQualifiers><Commission Amout="{markup}"/></MiscQualifiers>"""

    return commission_value
