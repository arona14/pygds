from enum import Enum
from typing import List


class PricingOption:
    pass


class OptionDetail(PricingOption):
    def __init__(self, attribute_type, passengers: List[str], segments: List[str]):
        self.attribute_type = attribute_type
        self.passengers = passengers
        self.segments = segments


class CarrierInformation(PricingOption):
    pass


class Currency(PricingOption):
    pass


class MonetaryInformation(PricingOption):
    pass


class DateInformation(PricingOption):
    pass


class FrequentFlyerInformation(PricingOption):
    pass


class FormOfPaymentInformation(PricingOption):
    pass


class CouponInformation(PricingOption):
    pass


class LocationInformation(PricingOption):
    pass


class PenDisInformation(PricingOption):
    pass


class PaxSegTstReference(PricingOption):
    pass


class TaxValueType(Enum):
    PERCENTAGE = "P"
    AMOUNT = "A"


class InformativeFareTax:
    def __init__(self, country, nature, rate, value_type: TaxValueType):
        self.country = country
        self.nature = nature
        self.rate = rate
        self.value_type = value_type

    def to_data(self):
        return {
            "country": self.country,
            "nature": self.nature,
            "rate": self.rate,
            "value_type": self.value_type
        }


class TaxInformation(PricingOption):
    def __init__(self, tax_infos: List[InformativeFareTax]):
        self.tax_infos = tax_infos
