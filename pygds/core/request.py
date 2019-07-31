from typing import List

from datetime import datetime

from pygds.core.types import TravellerNumbering, Itinerary, BasicDataObject



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
        self.city: str = ''

class OriginDestination:
    def __init__(self):
        self.departure_date: str = ''

class RequestedSegment:
    def __init__(self):
        self.origin: OriginDestination
        self.destination: OriginDestination
        self.departureDate: OriginDestination


class ClassOfService:
    def __init__(self):
        self.class_of_sevice: str = ''



class LowFareSearchRequest(BasicDataObject):

    def __init__(self, itineraries: List[RequestedSegment], csv: str = '',pcc: str = '', 
                adult: int = 0, child:int = 0, infant: int = 0, alternatePcc: list = [],
                requestType: str = '', preferredAirlines: list = [], baggagePref: bool = False,
        excludeBasicEconomy: bool = True):

 
        self.itineraries: List[RequestedSegment] = itineraries
        self.csv: ClassOfService = csv
        self.pcc = pcc 
        self.adult = adult
        self.child = child
        self.infant = infant 
        self.alternatePcc = alternatePcc
        self.requestType = requestType
        self.preferredAirlines = preferredAirlines
        self.baggagePref = baggagePref
        self.excludeBasicEconomy = excludeBasicEconomy

    def to_data(self):
        return {
            "itineraries": [i for i in self.itineraries],
            "pcc": self.pcc,
            "adult": self.adult,
            "child" : self.child,
            "infant" : self.infant,
            "csv": self.csv,
            "alternatePcc": [al for al in self.alternatePcc],
            "requestType" : self.requestType,
            "preferredAirlines" : self.preferredAirlines,
            "baggagePref" : self.baggagePref,
            "excludeBasicEconomy" : self.excludeBasicEconomy

        }

if __name__ == "__main__":
    print(LowFareSearchRequest().to_data())
