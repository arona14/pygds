from typing import List
from datetime import date


class PriceInfoBasic:
    def __str__(self):
        return str(self.to_dict())

    def to_dict(self):
        raise NotImplementedError("Not implemented")

    def __repr__(self):
        return str(self.to_dict())


class InformativePricing(PriceInfoBasic):
    def __init__(self, conversion_rate_details: str, indicators: str, number_of_pax: str, pricing_indicators: str,
                 fare_amount: str, segment_information: dict, fare_component_details: dict):
        self.conversion_rate_details = conversion_rate_details,
        self.indicators = indicators,
        self.number_of_pax = number_of_pax,
        self.pricing_indicators = pricing_indicators,
        self.fare_amount = fare_amount,
        self.segment_information = segment_information,
        self.fare_component_details = fare_component_details

    def to_dict(self):
        return {
            "conversion_rate_details": self.conversion_rate_details,
            "indicators": self.indicators,
            "number_of_pax": self.number_of_pax,
            "pricing_indicators": self.pricing_indicators,
            "fare_amount": self.fare_amount,
            "segment_information": self.segment_information,
            "fare_component_details": self.fare_component_details
        }


class PriceRequest(PriceInfoBasic):
    """
    A class to hold information about request of price PNR with booking class
    """

    def __init__(self, passengers: List[str], segments: List[str], fare_type: str = "PUB", baggage: int = 0, region_name: str = ""):
        self.passengers = passengers
        self.segments = segments
        self.fare_type = fare_type
        self.baggage = baggage
        self.region_name = region_name

    def to_dict(self):
        return {
            "passengers": self.passengers,
            "segments": self.segments,
            "fare_type": self.fare_type,
            "baggage": self.baggage,
            "region_name": self.region_name
        }


class FareAmount(PriceInfoBasic):
    """
        A class to hold information about an amount and its related currency
    """

    def __init__(self, qualifier: str = None, amount: float = 0.0, currency: str = None):
        self.qualifier: str = qualifier         # An internal qualifier
        self.amount: float = amount             # The amount
        self.currency: str = currency           # the currency specified

    def to_dict(self):
        return {
            "qualifier": self.qualifier,
            "amount": self.amount,
            "currency": self.currency
        }


class TaxInformation(PriceInfoBasic):
    """
        A class to represent tax information
    """

    def __init__(self):
        self.tax_qualifier: str = None       # The internal qualifier of the tax
        self.tax_identifier: str = None      # The identifier of the tax
        self.tax_type: str = None            # The type of the tax
        self.tax_nature: str = None          # The nature of the tax
        self.tax_amount: FareAmount = None   # The amount of that tax

    def to_dict(self):
        return {
            "tax_qualifier": self.tax_qualifier,
            "tax_identifier": self.tax_identifier,
            "tax_type": self.tax_type,
            "tax_nature": self.tax_nature,
            "tax_amount": None if not self.tax_amount else self.tax_amount.to_dict()
        }


class WarningInformation(PriceInfoBasic):
    """
        A class to specify a warning on a price proposal
    """

    def __init__(self):
        self.error_code: str            # The application error code
        self.qualifier: str             # The application code qualifier
        self.responsible_agency: str    # The application responsible agency
        self.warning: str               # The text of the warning

    def to_dict(self):
        return {
            "error_code": self.error_code,
            "qualifier": self.qualifier,
            "responsible_agency": self.responsible_agency,
            "warning": self.warning
        }


class CouponDetails(PriceInfoBasic):
    def __init__(self):
        self.coupon_product_type: str       # The product type of the coupon
        self.coupon_product_id: int         # The product id of the coupon

    def to_dict(self):
        return {
            "coupon_product_type": self.coupon_product_type,
            "coupon_product_id": self.coupon_product_id
        }


class FareComponent(PriceInfoBasic):
    """
        A class to describe a component of a fare. The components explain the fare
    """

    def __init__(self):
        self.item_number: int                   # The number of the component
        self.item_type: str                     # The type of the component
        self.departure: str                     # The departure (city or airport)
        self.arrival: str                       # The arrival (city or airport)
        self.monetary_info: FareAmount          # The amount
        self.rate_tariff_class: str             # Rate tariff class
        self.fare_qualifier: str                # The internal qualifier of the fare
        self.fare_family_name: str              # The name of the family fare
        self.fare_family_hierarchy: str         # The hierarchy of the family fare
        self.fare_family_owner: str             # The owner of the family fare
        self.coupons: List[CouponDetails] = []  # list of coupons

    def to_dict(self):
        return {
            "item_number": self.item_number,
            "item_type": self.item_type,
            "departure": self.departure,
            "arrival": self.arrival,
            "monetary_info": None if not self.monetary_info else self.monetary_info.to_dict(),
            "rate_tariff_class": self.rate_tariff_class,
            "fare_qualifier": self.fare_qualifier,
            "fare_family_name": self.fare_family_name,
            "fare_family_hierarchy": self.fare_family_hierarchy,
            "fare_family_owner": self.fare_family_owner,
            "coupons": [c.to_dict() for c in self.coupons],
        }


class ValidityInformation(PriceInfoBasic):
    """
    This will gather information about the validity of a price
    """

    def __init__(self):
        self.business_semantic: str     # an internal codification with semantic
        self.date: date                 # The date of validity

    def to_dict(self):
        return {
            "business_semantic": self.business_semantic,
            "date": self.date
        }


class SegmentInformation:
    def __init__(self):
        self.segment_reference: str                     # The reference of the segment
        self.segment_sequence_number: int               # The sequence number of the segment
        self.connection_type: str                       # The connection type
        self.class_of_service: str                      # class of service
        self.fare_basis_primary_code: str               # primary code of the fare basis
        self.fare_basis_code: str                       # code of fare basis
        self.fare_basis_ticket_designator: str          # ticket designator of the fare basis
        self.validity_infos: List[ValidityInformation] = []  # list of validity information
        self.baggage_allowance_quantity: int            # quantity of baggage allowance
        self.baggage_allowance_type: str                # type of baggage allowance

    def to_dict(self):
        return {
            "segment_reference": self.segment_reference,
            "segment_sequence_number": self.segment_sequence_number,
            "connection_type": self.connection_type,
            "class_of_service": self.class_of_service,
            "fare_basis_primary_code": self.fare_basis_primary_code,
            "fare_basis_code": self.fare_basis_code,
            "fare_basis_ticket_designator": self.fare_basis_ticket_designator,
            "validity_infos": [v.to_dict() for v in self.validity_infos],
            "baggage_allowance_quantity": self.baggage_allowance_quantity,
            "baggage_allowance_type": self.baggage_allowance_type
        }


class Fare(PriceInfoBasic):
    """
    A class to describe a price proposal
    """

    def __init__(self):
        self.fare_reference: str = None                        # the reference of the fare. To use on TST
        self.origin: str = None                                # The origin
        self.destination: str = None                           # the destination
        self.validating_carrier: str = None                    # The validating company
        self.pax_references: List[str] = []             # list of passenger references
        self.fare_amounts: List[FareAmount] = []        # List of fare amounts
        self.tax_infos: List[TaxInformation] = []       # List of tax information
        self.banker_rate: float = None                         # A rate of the banker
        self.warning_infos: List[WarningInformation] = []    # list of warning info
        self.segment_infos: List[SegmentInformation] = []    # list of segments
        self.fare_components: List[FareComponent] = []      # list of fare components

    def to_dict(self):
        return {
            "fare_reference": self.fare_reference,
            "origin": self.origin,
            "destination": self.destination,
            "validating_carrier": self.validating_carrier,
            "banker_rate": self.banker_rate,
            "pax_references": self.pax_references,
            "fare_amounts": [f.to_dict() for f in self.fare_amounts],
            "tax_infos": [t.to_dict() for t in self.tax_infos],
            "warning_infos": [w.to_dict() for w in self.warning_infos],
            "segment_infos": [s.to_dict() for s in self.segment_infos],
            "fare_components": [c.to_dict() for c in self.fare_components]
        }


class TstInformation(PriceInfoBasic):
    """
    This class will store information about A created TST
    """

    def __init__(self, pnr, tst_ref: str, pax_refs: List[str]):
        """
        Init
        :param pnr: The record locator (str)
        :param tst_ref: the TST reference (str)
        :param pax_refs: list of passenger references (list of str)
        """
        self.pnr = pnr
        self.tst_reference = tst_ref
        self.pax_references = pax_refs if pax_refs else []

    def to_dict(self):
        return {
            "pnr": self.pnr,
            "tst_reference": self.tst_reference,
            "pax_references": self.pax_references
        }


class SearchPriceInfos(PriceInfoBasic):
    """
        This class we will get the Info of Search price
    """

    def __init__(self):
        self.status: str = None  # the status of result
        self.air_itinerary_pricing_info: AirItineraryPricingInfo  # the aount of air itinenary pricing

    def to_dict(self):
        return {
            "status": self.status,
            "air_itinerary_pricing_info": self.air_itinerary_pricing_info
        }


class FareElement(PriceInfoBasic):

    def __init__(self, primary_code, connection, not_valid_before, not_valid_after, baggage_allowance, fare_basis):
        self.primary_code = primary_code
        self.connection = connection
        self.not_valid_before = not_valid_before
        self.not_valid_after = not_valid_after
        self.baggage_allowance = baggage_allowance
        self.fare_basis = fare_basis

    def to_dict(self):
        return {
            "primary_code": self.primary_code,
            "connection": self.connection,
            "not_valid_before": self.not_valid_before,
            "not_valid_after": self.not_valid_after,
            "baggage_allowance": self.baggage_allowance,
            "fare_basis": self.fare_basis
        }


class AirItineraryPricingInfo(PriceInfoBasic):
    """
    This class we will get the amount of price
    """

    def __init__(self):
        self.base_fare: float = 0.0       # base fare amount
        self.taxes: float = 0.0            # taxes amount
        self.total_fare: float             # totoal fare amount
        self.currency_code: str = None     # currency code
        self.passenger_type: str = None     # passenger type
        self.passenger_quantity: str = None  # passenger quantity
        self.charge_amount: float = 0.0      # Charge Amount
        self.tour_code: str = None            # Tour Code
        self.ticket_designator: str = None    # Ticket Designator
        self.commission_percentage: str = None  # Commission Percentage
        self.fare_break_down: FareBreakdown     # FareBreakdown class
        self.valiating_carrier: str = None     # passenger type
        self.baggage_provisions: list = []

    def to_dict(self):
        return{
            "base_fare": self.base_fare,
            "taxes": self.taxes,
            "total_fare": self.total_fare,
            "currency_code": self.currency_code,
            "passenger_type": self.passenger_type,
            "passenger_quantity": self.passenger_quantity,
            "charge_amount": self.charge_amount,
            "tour_code": self.tour_code,
            "ticket_designator": self.ticket_designator,
            "commission_percentage": self.commission_percentage,
            "valiating_carrier": self.valiating_carrier,
            "fare_break_down": self.fare_break_down,
            "baggage_provisions": self.baggage_provisions
        }


class FareBreakdown(PriceInfoBasic):

    """
    In this class we will get the fare Break Down
    """

    def __init__(self):

        self.cabin: str = None               # the cabin class
        self.fare_basis_code: str = None     # fare basis Code
        self.fare_amount: str = None         # fare amount
        self.fare_passenger_type: str = None  # fare passenger type
        self.fare_type: str = None           # fare type
        self.filing_carrier: str = None      # Filing Carrier
        self.free_baggage: str = None      # Filing Carrier

    def to_dict(self):
        return {
            "cabin": self.cabin,
            "fare_basis_code": self.fare_basis_code,
            "fare_amount": self.fare_amount,
            "fare_passenger_type": self.fare_passenger_type,
            "fare_type": self.fare_type,
            "filing_carrier": self.filing_carrier,
            "free_baggage": self.free_baggage
        }
