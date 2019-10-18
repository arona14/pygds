
from typing import List


class FlightSegment:
    " the flight Segment class"
    def __init__(self):
        self.arrival_date_time: str
        self.departure_date_time: str
        self.flight_number: str
        self.number_in_party: str
        self.res_book_desig_code: str
        self.status: str
        self.destination_location: str
        self.marketing_airline: str
        self.marriage_grp: str
        self.operating_airline: str
        self.origin_location: str

    def to_dict(self):
        return {
            "ArrivalDateTime": self.arrival_date_time,
            "DepartureDateTime": self.departure_date_time,
            "FlightNumber": self.flight_number,
            "NumberInParty": self.number_in_party,
            "ResBookDesigCode": self.res_book_desig_code,
            "Status": self.status,
            "DestinationLocation": {
                "LocationCode": self.destination_location
            },
            "MarketingAirline": {
                "Code": self.marketing_airline,
                "FlightNumber": self.flight_number
            },
            "MarriageGrp": self.marriage_grp,
            "OperatingAirline": {
                "Code": self.operating_airline
            },
            "OriginLocation": {
                "LocationCode": self.origin_location
            }
        }


class PassengerFare:
    """
        Passenger fare  class
    """
    def __init__(self):
        self.name_number: str
        self.given_name: str
        self.surname: str
        self.date_of_birth: str
        self.gender: str
        self.passenger_type: str
        self.amount: float
        self.percent: str
        self.ticket_designator: str
        self.tour_code: str
        self.total_fare: float
        self.service_fee: float
        self.phone: str
        self.email: str
        self.address: str
        self.middle_name: str
        self.brand_id: str

    def to_dict(self):
        return {
            "NameNumber": self.name_number,
            "GivenName": self.given_name,
            "Surname": self.surname,
            "DateOfBirth": self.date_of_birth,
            "Gender": self.gender,
            "PassengerType": self.passenger_type,
            "Amount": self.amount,
            "Percent": self.percent,
            "TicketDesignator": self.ticket_designator,
            "TourCode": self.tour_code,
            "TotalFare": self.total_fare,
            "ServiceFee": self.service_fee,
            "Phone": self.phone,
            "Email": self.email,
            "Address": self.address,
            "MiddleName": self.middle_name
        }


class CreatePnrRequest:

    """
        the class who build the create pnr resquest
    """

    def __init__(self, flight_segments: List[FlightSegment], passengers: List[PassengerFare], remarks: List[dict], target_city: str, fare_type: str, customer_identifier: str, brand_id: str, user, last_ticket_date):

        self.flight_segments = flight_segments
        self.passengers = passengers
        self.remarks = remarks
        self.target_city = target_city
        self.fare_type = fare_type
        self.customer_identifier = customer_identifier
        self.user = user
        self.last_ticket_date = last_ticket_date
        self.brand_id = brand_id

    def to_dict(self):
        return {
            "FlightSegment": self.flight_segments,
            "Passengers": self.passengers,
            "Remarks": self.remarks,
            "TargetCity": self.target_city,
            "FareType": self.fare_type,
            "CustomerIdentifier": self.customer_identifier,
            "LastTicketDate": self.last_ticket_date,
            "Brand": self.brand_id

        }
