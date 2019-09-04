from typing import List
from types import SimpleNamespace
from pygds.core.types import TravellerNumbering, BasicDataObject


class RequestFilter:
    pass


class AirlineFilter(RequestFilter):
    def __init__(self):
        self.target_airlines: List[str] = []
        self.exclude_airlines: List[str] = []


class TimeWindow:
    def __init__(self):
        self.category: str = ''  # day or hour
        self.value: int = 0


class FlightCategoryFilter(RequestFilter):
    def __init__(self):
        self.with_stops: bool = False
        self.connecting_flight: List[str] = []


class ConnectingPointFilter(RequestFilter):
    def __init__(self):
        self.include_connecting_points: List[str] = []
        self.exclude_connecting_points: List[str] = []
        self.preferred_connecting_points: List[str] = []


class CabinClassFilter:
    def __init__(self):
        self.desired_cabin_classes: str = ''


class FareTypeFilter(RequestFilter):
    def __init__(self):
        self.no_advance_purchase = False  # NAP
        self.no_penalty = False  # NPE
        self.no_restriction = False  # NR
        self.no_refundable = False  # RF


class PriceToBeatFilter(RequestFilter):
    def __init__(self):
        self.total_amount: float = 0


class OriginDestination:
    def __init__(self):
        self.origin: str = ''


class OriginDestination_:
    def __init__(self):
        self.departure_date: str = ''


class RequestedSegment:
    def __init__(self, sequence: str = None, origin: str = None, destination: str = None, departure_date: str = None, arrival_date: str = None, total_seats: str = None):
        self.sequence = sequence
        self.origin = origin
        self.destination = destination
        self.departure_date = departure_date
        self.arrival_date = arrival_date
        self.total_seats = total_seats

    def to_data(self):
        return {
            "sequence": self.sequence,
            "origin": self.origin,
            "destination": self.destination,
            "departure_date": self.departure_date,
            "arrival_date": self.arrival_date,
            "total_seats": self.total_seats
        }


class ClassOfService:
    def __init__(self):
        self.class_of_sevice: str = ''


class TravellerNumberingInfo(TravellerNumbering):

    def __init__(self, adults, children, infants):
        super().__init__(adults, children, infants)

    def to_data(self):

        return SimpleNamespace(**{
            "adult": self.adults,
            "child": self.children,
            "infant": self.infants,
        })


class LowFareSearchRequest(BasicDataObject):

    def __init__(self, itineraries: List[RequestedSegment], csv, pcc,
                 travelingNumber: TravellerNumberingInfo = None, alternatePcc: list = [],
                 requestType: str = '', preferredAirlines: list = [], baggagePref: bool = False,
                 excludeBasicEconomy: bool = True, maxConnection: int = 3):

        self.itineraries: List[RequestedSegment] = itineraries
        self.csv = csv
        self.pcc = pcc
        self.adult = travelingNumber.adults
        self.child = travelingNumber.children
        self.infant = travelingNumber.infants
        self.alternatePcc = alternatePcc
        self.requestType = requestType
        self.preferredAirlines = preferredAirlines
        self.baggagePref = baggagePref
        self.excludeBasicEconomy = excludeBasicEconomy
        self.maxConnection = maxConnection

    def to_data(self):
        return SimpleNamespace(**{
            "itineraries": [i for i in self.itineraries],
            "pcc": self.pcc,
            "adult": self.adult,
            "child": self.child,
            "infant": self.infant,
            "csv": self.csv,
            "alternatePcc": [al for al in self.alternatePcc],
            "requestType": self.requestType,
            "preferredAirlines": self.preferredAirlines,
            "baggagePref": self.baggagePref,
            "excludeBasicEconomy": self.excludeBasicEconomy
        })
