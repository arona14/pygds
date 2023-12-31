from typing import List
from pygds.core.types import TravellerNumbering, BasicDataObject, FareOptions, TravelFlightInfo


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
    """ airportCityQualifier
        A Airport
        C City
    """

    def __init__(self, sequence: int = 1, origin: str = None, destination: str = None, departure_date: str = None, arrival_date: str = None, total_seats: str = None, airport_city_qualifier: str = "A"):
        self.airport_city_qualifier = airport_city_qualifier
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

        return {
            "adult": self.adults,
            "child": self.children,
            "infant": self.infants,
        }


class LowFareSearchRequest(BasicDataObject):

    def __init__(self, itineraries: List[RequestedSegment], csv: str = "Y", pcc: str = None,
                 travelingNumber: TravellerNumberingInfo = None, alternatePcc: list = [],
                 requestType: str = "", preferredAirlines: list = [], baggagePref: bool = False,
                 excludeBasicEconomy: bool = True, maxConnection: int = 3, number_of_unit_rc: str = 50,
                 fare_options: FareOptions = None, travel_flight_info: TravelFlightInfo = None):

        self.travel_flight_info = travel_flight_info
        self.fare_options = fare_options
        self.number_of_unit_rc = number_of_unit_rc
        self.itineraries: List[RequestedSegment] = itineraries
        self.csv = csv  # the class of service/the cabine class
        self.pcc = pcc
        self.travelingNumber = travelingNumber
        self.alternatePcc = alternatePcc
        self.requestType = requestType  #
        self.preferredAirlines = preferredAirlines  # carrierId in Amadeus
        self.baggagePref = baggagePref
        self.excludeBasicEconomy = excludeBasicEconomy
        self.maxConnection = maxConnection

    @property
    def adult(self):
        return self.travelingNumber.adults

    @property
    def child(self):
        return self.travelingNumber.children

    @property
    def infant(self):
        return self.travelingNumber.infants

    def to_data(self):
        return {
            "itineraries": [i for i in self.itineraries],
            "pcc": self.pcc,
            "adult": self.adult,
            "child": self.child,
            "infant": self.infant,
            "csv": self.csv,
            "alternate_pcc": [al for al in self.alternatePcc],
            "request_type": self.requestType,
            "preferred_airlines": [pref for pref in self.preferredAirlines],
            "baggage_pref": self.baggagePref,
            "exclude_basic_economy": self.excludeBasicEconomy,
            "max_connection": self.maxConnection
        }
