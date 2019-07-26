from typing import List
from datetime import date


class PriceInfoBasic:
    def __str__(self):
        return str(self.__repr__())


class FareAmount(PriceInfoBasic):
    """
        A class to hold information about an amount and its related currency
    """
    def __init__(self):
        self.qualifier: str         # An internal qualifier
        self.amount: float = 0.0    # The amount
        self.currency: str          # the currency specified

    def __repr__(self):
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
        self.tax_qualifier: str        # The internal qualifier of the tax
        self.tax_identifier: str       # The identifier of the tax
        self.tax_type: str             # The type of the tax
        self.tax_nature: str           # The nature of the tax
        self.tax_amount: FareAmount    # The amount of that tax

    def __repr__(self):
        return {
            "tax_qualifier": self.tax_qualifier,
            "tax_identifier": self.tax_identifier,
            "tax_type": self.tax_type,
            "tax_nature": self.tax_nature,
            "tax_amount": None if not self.tax_amount else self.tax_amount.__repr__()
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

    def __repr__(self):
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

    def __repr__(self):
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

    def __repr__(self):
        return {
            "item_number": self.item_number,
            "item_type": self.item_type,
            "departure": self.departure,
            "arrival": self.arrival,
            "monetary_info": None if not self.monetary_info else self.monetary_info.__repr__(),
            "rate_tariff_class": self.rate_tariff_class,
            "fare_qualifier": self.fare_qualifier,
            "fare_family_name": self.fare_family_name,
            "fare_family_hierarchy": self.fare_family_hierarchy,
            "fare_family_owner": self.fare_family_owner,
            "coupons": [c.__repr__() for c in self.coupons],
        }


class ValidityInformation(PriceInfoBasic):
    """
    This will gather information about the validity of a price
    """
    def __init__(self):
        self.business_semantic: str     # an internal codification with semantic
        self.date: date                 # The date of validity

    def __repr__(self):
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

    def __repr__(self):
        return {
            "segment_reference": self.segment_reference,
            "segment_sequence_number": self.segment_sequence_number,
            "connection_type": self.connection_type,
            "class_of_service": self.class_of_service,
            "fare_basis_primary_code": self.fare_basis_primary_code,
            "fare_basis_code": self.fare_basis_code,
            "fare_basis_ticket_designator": self.fare_basis_ticket_designator,
            "validity_infos": [v.__repr__() for v in self.validity_infos],
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

    def __repr__(self):
        return {
            "fare_reference": self.fare_reference,
            "origin": self.origin,
            "destination": self.destination,
            "validating_carrier": self.validating_carrier,
            "banker_rate": self.banker_rate,
            "pax_references": self.pax_references,
            "fare_amounts": [f.__repr__() for f in self.fare_amounts],
            "tax_infos": [t.__repr__() for t in self.tax_infos],
            "warning_infos": [w.__repr__() for w in self.warning_infos],
            "segment_infos": [s.__repr__() for s in self.segment_infos],
            "fare_components": [c.__repr__() for c in self.fare_components]
        }
