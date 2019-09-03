def passenger_info(date_of_birth, gender, name_number, first_name, last_name):
    return f"""<SecureFlight SegmentNumber="A">
     <PersonName DateOfBirth="{date_of_birth}" Gender="{gender}" NameNumber="{name_number}">
     <GivenName>{first_name}</GivenName>
     <Surname>{last_name}</Surname>
     </PersonName>
     </SecureFlight>"""


def customer_id(dk_number):
    return f"""<TravelItineraryAddInfoRQ>
         <CustomerInfo>
            <CustomerIdentifier>{dk_number}</CustomerIdentifier>
         </CustomerInfo>
     </TravelItineraryAddInfoRQ>"""


def service_ssr_code(segment_number, ssr_code, name_number):
    return f"""<Service SegmentNumber="{segment_number}" SSR_Code="{ssr_code}">
                 <PersonName NameNumber="{name_number}"/>
            </Service>"""


def seat_request(name_number, seat_number, segment_number):
    return f"""<Seat NameNumber="{name_number}" Number="{seat_number}" SegmentNumber="{segment_number}"/>"""


class PassengerUpdate:
    def __init__(self):
        self.name_number: str = None
        self.dk_number: str = None
        self.date_of_birth: str = None
        self.gender: str = None
        self.first_name: str = None
        self.last_name: str = None
        self.segment_number: str = None
        self.ssr_code: str = None
        self.seat_number: str = None
