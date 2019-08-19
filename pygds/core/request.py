from typing import List
from types import SimpleNamespace
from datetime import datetime

#from pygds.core.types import TravellerNumbering, Itinerary, BasicDataObject
from pygds.core.type_helper import TravellerNumbering, Itinerary, BasicDataObject


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


class RequestedSegment:
    def __init__(self, origin, destination, departureDate):
        self.origin = origin
        self.destination = destination
        self.departureDate = departureDate

    def to_data(self):
        return {
            "origin": self.origin,
            "destination": self.destination,
            "departureDate": self.departureDate
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
            "preferredAirlines": [pref for pref in self.preferredAirlines],
            "baggagePref": self.baggagePref,
            "excludeBasicEconomy": self.excludeBasicEconomy,
            "maxConnection": self.maxConnection

        })


if __name__ == "__main__":
    pass
    passenger1 = RequestedSegment("DTW", "NYC", "20-10-2019")
    #passenger = RequestedSegment("DTW", "NYC", "20-10-2019").to_data()
    #[{'origin': 'DTW', 'destination': 'NYC', 'departureDate': '20-10-2019'}]
    #passenger = passenger.append(passenger1)
    #passenger = passenger.append(passenger1)
    #passenger = passenger.append({"DTW","NYC","20-10-2019"})
    # print(passenger)
    # print(passenger1)
    g = TravellerNumberingInfo(1, 3, 4)
    y = LowFareSearchRequest(passenger1, "", "WR17", g, [], "sds", [], False, True).to_data()
    print(y)
    #                                                                                                                                                                                                                                                   print(passenger1)
