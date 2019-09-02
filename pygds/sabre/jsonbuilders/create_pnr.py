
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


class Passengers:
    """
        Passengers class
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
        self.base_fare: float
        self.total_fare: float
        self.service_fee: float
        self.charge_amount: float
        self.phone: str
        self.email: str
        self.address: str
        self.nationality: str
        self.title: str
        self.middle_name: str
        self.deals: Deals()

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
            "BaseFare": self.base_fare,
            "TotalFare": self.total_fare,
            "ServiceFee": self.service_fee,
            "ChargeAmount": self.charge_amount,
            "Phone": self.phone,
            "Email": self.email,
            "Address": self.address,
            "Nationality": self.nationality,
            "Title": self.title,
            "MiddleName": self.middle_name,
            "deals": self.deals.to_dict()
        }


class Deals:
    """
    the Deals class
    """
    def __init__(self):
        self.cts_reward: float
        self.cts_markup: float
        self.agency_markup: float
        self.agency_discount: float

    def to_dict(self):
        return {
            "cts_reward": self.cts_reward,
            "cts_markup": self.cts_markup,
            "agency_markup": self.agency_markup,
            "agency_discount": self.agency_discount
        }


class CreatePnrRequest:

    """
        the class who build the create pnr resquest
    """

    def __init__(self, flight_segments: List[FlightSegment], passengers: List[Passengers], remarks: list, target_city: str, fare_type: str, customer_identifier: str, destination: str, bags: str, refund, refund_before, refund_after, exchange, exchange_after, exchange_before, airline, user, last_ticket_date, commission):

        self.flight_segments = flight_segments
        self.passengers = passengers
        self.remarks = remarks
        self.target_city = target_city
        self.fare_type = fare_type
        self.customer_identifier = customer_identifier
        self.destination = destination
        self.bags = bags
        self.refund = refund
        self.refund_before = refund_before
        self.refund_after = refund_after
        self.exchange = exchange
        self.exchange_before = exchange_before
        self.exchange_after = exchange_after
        self.airline = airline
        self.user = user
        self.last_ticket_date = last_ticket_date
        self.commission = commission

    def to_dict(self):
        return {
            "FlightSegment": self.flight_segments,
            "Passengers": self.passengers,
            "Remarks": self.remarks,
            "TargetCity": self.target_city,
            "FareType": self.fare_type,
            "CustomerIdentifier": self.customer_identifier,
            "Destination": self.destination,
            "Bags": self.bags,
            "Refund": self.refund,
            "RefundAfter": self.refund_after,
            "RefundBefore": self.refund_before,
            "Exchange": self.exchange,
            "ExchangeAfter": self.exchange_after,
            "ExchangeBefore": self.exchange_before,
            "Airline": self.airline,
            "LastTicketDate": self.last_ticket_date,
            "Commission": self.commission
        }
