
from typing import List


class FlightSegment:
    " the flight Segment class"
    def __init__(self):
        self.flight_number: str
        self.departure_date_time: str
        self.arrival_date_time: str
        self.res_book_desig_code: str
        self.origin_location: str
        self.destination_location: str
        self.marketing_airline: str
        self.operating_airline: str

    def to_dict(self):
        return {
            "Number": self.flight_number,
            "DepartureDateTime": self.departure_date_time,
            "ArrivalDateTime": self.arrival_date_time,
            "Type": "A",
            "ClassOfService": self.res_book_desig_code,
            "OriginLocation": {
                "LocationCode": self.origin_location
            },
            "DestinationLocation": {
                "LocationCode": self.destination_location
            },
            "Airline": {
                "Operating": self.operating_airline,
                "Marketing": self.marketing_airline
            }
        }


class Itineraries():

    def __init__(self, rph: str, origin_location: str, destination_location: str, departure_date_time: str, flight_segments: List[FlightSegment]):
        self.rph = rph
        self.origin_location = origin_location
        self.destination_location = destination_location
        self.departure_date_time = departure_date_time
        self.flight_segments = flight_segments

    def to_dict(self):
        return {
            "RPH": self.rph,
            "OriginLocation": {
                "LocationCode": self.origin_location,
                "CodeContext": "IATA"
            },
            "DestinationLocation": {
                "LocationCode": self.destination_location,
                "CodeContext": "IATA"
            },
            "DepartureDateTime": self.departure_date_time,
            "TPA_Extensions": {
                "Flight": self.flight_segments
            }
        }
