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

    def __init__(self):
        self.origin_destination: List[OriginDestination] = []

    def to_data(self):
        return{
            "origin_destination": [s.to_data() for s in self.origin_destination]
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


class ChangeFeeCollectionOptions(BasicDataObject):

    def __init__(self, fee_collection_method):

        self.fee_collection_method = fee_collection_method

    def to_data(self):
        return {
            "fee_collection_method": self.fee_collection_method
        }


class ExchangeDetails(BasicDataObject):

    def __init__(self, change_fee: str = None, exchange_reissue: str = None, total_refund: str = None, change_fee_collectionOptions: ChangeFeeCollectionOptions = None):

        self.change_fee = change_fee
        self.exchange_reissue = exchange_reissue
        self.total_refund = total_refund
        self.change_fee_collectionOptions = change_fee_collectionOptions

    def to_data(self):

        return {
            "change_fee": self.change_fee,
            "exchange_reissue": self.exchange_reissue,
            "total_refund": self.total_refund,
            "change_fee_collectionOptions": self.change_fee_collectionOptions
        }


class TaxData(BasicDataObject):

    def __init__(self, amount: str = None, tax_code: str = None):
        self.amount = amount
        self.tax_code = tax_code

    def to_data(self):

        return {
            "amount": self.amount,
            "tax_code": self.tax_code
        }


class TaxComparison(BasicDataObject):

    def __init__(self, tax_type: str = None):
        self.tax_type = tax_type
        self.tax: List[TaxData] = []

    def to_data(self):

        return {
            "tax_type": self.tax_type,
            "tax": [t.to_data() for t in self.tax]
        }


class TotalFare(BasicDataObject):

    def __init__(self, amount: str = None):
        self.amount = amount

    def to_data(self):

        return {
            "amount": self.amount
        }


class Taxes(BasicDataObject):

    def __init__(self, total_amount: str = None):
        self.total_amount = total_amount

    def to_data(self):

        return {
            "total_amount": self.total_amount
        }


class BaseFare(BasicDataObject):

    def __init__(self, amount: str = None, currency_code: str = None):
        self.amount = amount
        self.currency_code = currency_code

    def to_data(self):

        return {
            "amount": self.amount,
            "currency_code": self.currency_code
        }


class ItinTotalFare(BasicDataObject):

    def __init__(self, base_fare: BaseFare = None, taxes: Taxes = None, total_fare: TotalFare = None):

        self.base_fare = base_fare
        self.taxes = taxes
        self.total_fare = total_fare

    def to_data(self):

        return {
            "base_fare": self.base_fare,
            "taxes": self.taxes,
            "total_fare": self.total_fare

        }


class ExchangeAirItineraryPricingInfo(BasicDataObject):

    def __init__(self, price_type: str = None, itin_total_fare: ItinTotalFare = None):

        self.price_type = price_type
        self.itin_total_fare = itin_total_fare


class ExchangeComparison(BasicDataObject):

    def __init__(self, pqr_number: str = None, exchange_details: ExchangeDetails = None):

        self.pqr_number = pqr_number
        self.air_itinerary_pricing_info: List[ExchangeAirItineraryPricingInfo] = []
        self.tax_comparison: List[TaxComparison] = []
        self.exchange_details = exchange_details

    def to_data(self):

        return {
            "pqr_number": self.pqr_number,
            "air_itinerary_pricing_info": [price.to_data() for price in self.air_itinerary_pricing_info],
            "tax_comparison": [t.to_data() for t in self.tax_comparison],
            "exchange_details": self.exchange_details
        }


class FreeBaggageAllowance(BasicDataObject):

    def __init__(self, number):
        self.number = number

    def to_data(self):
        return {
            "number": self.number
        }


class MarketingAirline(BasicDataObject):

    def __init__(self, code, flight_number):
        self.code = code
        self.flight_number = flight_number

    def to_data(self):
        return {
            "code": self.code,
            "flight_number": self.flight_number
        }


class ExchangeFlightSegment(BasicDataObject):

    def __init__(self, departure_date: str = None, arrival_date: str = None, origin: str = None, destination: str = None, flight_number: str = None, rph: str = None, segment_number: str = None, marketing_airline: MarketingAirline = None, free_baggage_allowance: FreeBaggageAllowance = None):
        self.departure_date = departure_date
        self.arrival_date = arrival_date
        self.origin = origin
        self.destination = destination
        self.flight_number = flight_number
        self.rph = rph
        self.segment_number = segment_number
        self.marketing_airline = marketing_airline
        self.free_baggage_allowance = free_baggage_allowance

    def to_data(self):
        return{
            "departure_date": self.departure_date,
            "arrival_date": self.arrival_date,
            "origin": self.origin,
            "destination": self.destination,
            "flight_number": self.flight_number,
            "rph": self.rph,
            "segment_number": self.segment_number,
            "marketing_airline": self.marketing_airline,
            "free_baggage_allowance": self.free_baggage_allowance

        }


class BaggageInfo(BasicDataObject):

    def __init__(self):
        self.flight_segment: List[ExchangeFlightSegment] = []

    def to_data(self):
        return{
            "flight_segment": [s.to_data() for s in self.segments]

        }


class ExchangeComparisonInfos(BasicDataObject):
    """
        This class we will get the Info of Search price
    """
    def __init__(self, status: str = None, baggage_info: BaggageInfo = None, exchange_comparison: ExchangeComparison = None):
        self.status = status
        self.baggage_info = baggage_info
        self.exchange_comparison = exchange_comparison

    def to_data(self):
        return {
            "status": self.status,
            "baggage_info": self.baggage_info,
            "exchange_comparison": self.exchange_comparison
        }
