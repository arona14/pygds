from enum import Enum
from typing import List


class OptionDetail():
    """
    Hold information of option details
    """
    def __init__(self, attribute_type: str, passengers: List[str], segments: List[str]):
        self.attribute_type = attribute_type
        self.passengers = passengers
        self.segments = segments

    def to_data(self):
        return {
            "attribute_type": self.attribute_type,
            "passengers": self.passengers,
            "segments": self.segments
        }


class TaxValueType(Enum):
    """
    Hold infomation of tax value type
    """
    PERCENTAGE = "P"
    AMOUNT = "A"


class InformativeFareTax:
    """
    Hold information of Informative Fare Tax
    """
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


class TaxInformation():
    """
    Hold information of Tax
    """
    def __init__(self, tax_infos: List[InformativeFareTax]):
        self.tax_infos = tax_infos

    def to_data(self):
        return {
            "tax_info": self.tax_infos
        }
