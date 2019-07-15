from typing import List

from datetime import datetime

from pygds.core.types import TravellerNumbering, Itinerary


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


class CabinClassFilter(RequestFilter):
    def __init__(self):
        self.desired_cabin_classes: List[str] = []


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
        self.airport: str = ''
        self.alternates: List[str] = []
        self.radius: float = 0.0  # 300 km maximum
        self.is_multi_city: bool = False  # like QLA, QSF
        self.date_time: datetime
        self.time_window: TimeWindow


class RequestedSegment:
    def __init__(self):
        self.origin: OriginDestination
        self.destination: OriginDestination
        self.flight_category_filter: FlightCategoryFilter
        self.connecting_point_filter: ConnectingPointFilter


class RequestedItinerary:
    def __init__(self):
        self.segments: List[RequestedSegment] = []
        self.airline_filter: AirlineFilter
        self.flight_category_filter: FlightCategoryFilter
        self.cabin_filter: CabinClassFilter
        self.fare_filter: FareTypeFilter
        self.price_to_beat: PriceToBeatFilter


class LowFareSearchRequest:
    def __init__(self, itineraries: List[RequestedItinerary], numbering: TravellerNumbering,
                 filters: List[RequestFilter] = None, currency_conversion: str = None,
                 maximum_recommendations: int = 200):
        if filters is None:
            filters = []
        self.itineraries: List[RequestedItinerary] = itineraries
        self.numbering: TravellerNumbering = numbering
        self.filters: List[RequestFilter] = filters
        self.currency_conversion: str = currency_conversion
        self.maximum_recommendations: int = maximum_recommendations
