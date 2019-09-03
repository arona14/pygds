from typing import List
from pygds.core.types import BasicDataObject


class PriceDifference(BasicDataObject):

    def __init__(self, currency_code: str = None, value: str = None):
        self.currency_code = currency_code
        self.value = value

    def to_data(self):

        return {
            "currency_code": self.currency_code,
            "value": self.value
        }


class TotalPriceDifference(BasicDataObject):

    def __init__(self, sub_total_difference: PriceDifference = None, total_fee: PriceDifference = None, grand_total_difference: PriceDifference = None):

        self.sub_total_difference = sub_total_difference
        self.total_fee = total_fee
        self.grand_total_difference = grand_total_difference

    def to_data(self):
        return {
            "sub_total_difference": self.sub_total_difference,
            "total_fee": self.total_fee,
            "grand_total_difference": self.grand_total_difference
        }


class Fare(BasicDataObject):

    def __init__(self, valid: str = None, total_price_difference: TotalPriceDifference = None):
        self.valid = valid
        self.total_price_difference = total_price_difference

    def to_data(self):
        return {
            "valid": self.valid,
            "total_price_difference": self.total_price_difference

        }


class ReservationSegment(BasicDataObject):

    def __init__(self, segment_number: str = None, elapsed_time: str = None, departure_date: str = None, arrival_date: str = None, origin: str = None, destination: str = None, marketing_flight_number: str = None, marketing: str = None, operating: str = None):
        self.segment_number = segment_number
        self.elapsed_time = elapsed_time
        self.departure_date = departure_date
        self.arrival_date = arrival_date
        self.origin = origin
        self.destination = destination
        self.marketing_flight_number = marketing_flight_number
        self.marketing = marketing
        self.operating = operating

    def to_data(self):
        return{
            "segment_number": self.segment_number,
            "elapsed_time": self.elapsed_time,
            "departure_date": self.departure_date,
            "arrival_date": self.arrival_date,
            "origin": self.origin,
            "destination": self.destination,
            "marketing_flight_number": self.marketing_flight_number,
            "marketing": self.marketing,
            "operating": self.operating

        }


class OriginDestination(BasicDataObject):

    def __init__(self):
        self.segments: List[ReservationSegment] = []

    def to_data(self):
        return{
            "segments": [s.to_data() for s in self.segments]

        }


class BookItinerary(BasicDataObject):

    def __init__(self, origin_destination: OriginDestination = None):
        self.origin_destination = origin_destination

    def to_data(self):
        return{
            "origin_destination": self.origin_destination
        }


class ExchangeData(BasicDataObject):

    def __init__(self, sequence: str = None, book_itinerary: BookItinerary = None, fare: Fare = None):

        self.sequence = sequence
        self.book_itinerary = book_itinerary
        self.fare = fare

    def to_data(self):
        return{
            "sequence": self.sequence,
            "book_itinerary": self.book_itinerary,
            "fare": self.fare

        }


class ExchangeShoppingInfos(BasicDataObject):
    """
        This class we will get the Info of Search price
    """
    def __init__(self, status, exchange):
        self.status = status
        self.exchange = exchange

    def to_data(self):
        return {
            "status": self.status,
            "exchange": self.exchange
        }
