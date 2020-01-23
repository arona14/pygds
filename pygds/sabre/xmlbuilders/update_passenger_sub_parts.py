def passenger_info(date_of_birth, gender, name_number, first_name, last_name):
    return f"""<SecureFlight SegmentNumber="A">
     <PersonName DateOfBirth="{date_of_birth}" Gender="{gender}" NameNumber="{name_number}">
     <GivenName>{first_name}</GivenName>
     <Surname>{last_name}</Surname>
     </PersonName>
     </SecureFlight>"""


def cust_loyalty_info(member_ship_id: str = "", name_number: str = "", program_id: str = "", segment_number: int = 1):
    if member_ship_id and name_number and program_id:
        return f"""
                <CustLoyalty MembershipID="{member_ship_id}" NameNumber="{name_number}" ProgramID="{program_id}" SegmentNumber="{segment_number}"/>
                """
    return ""


def customer_id(dk_number: str):
    return f"""
            <CustomerIdentifier>{dk_number}</CustomerIdentifier>
         """


def travel_itinerary_add_info_rq(dk_number: str = "", member_ship_id: str = "", name_number: str = "", program_id: str = "", segment_number: int = 1):
    customer_identifier = customer_id(dk_number) if dk_number else ""
    cust_loyalty = cust_loyalty_info(member_ship_id, name_number, program_id, segment_number)
    if customer_identifier or cust_loyalty:
        return f"""<TravelItineraryAddInfoRQ>
             <CustomerInfo>
                {customer_identifier}
                {cust_loyalty}
             </CustomerInfo>
         </TravelItineraryAddInfoRQ>"""
    return ""


def service_ssr_code(segment_number, ssr_code, name_number):
    return "\n".join([f"""<Service SegmentNumber="{segment_number}" SSR_Code="{ssr_cod}">
                 <PersonName NameNumber="{name_number}"/>
            </Service>""" for ssr_cod in ssr_code])


def seat_request(name_number, seat_number, segment_number):
    return f"""
                <AirSeatRQ>
                    <Seats>
                        <Seat NameNumber="{name_number}" Number="{seat_number}" SegmentNumber="{segment_number}"/>
                    </Seats>
                </AirSeatRQ>
            """
