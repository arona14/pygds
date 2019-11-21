from enum import Enum


class ContractType(Enum):
    TKT = "TKT"  # Ticket
    MCO = "MCO"  # Miscellaneous Charge Order
    EMD = "EMD"  # Electronic Miscellaneous Document
    XSB = "XSB"  # Excess Baggage
    TASF = "TASF"  # Travel Agent Service Fee


class ContractNature(Enum):
    DOMESTIC = "DOM"
    INTERNATIONAL = "INT"


class ContractMedia(Enum):
    MISCELLANEOUS_DOCUMENT = "ED"
    ELECTRONIC_TICKET = "ET"


class Contract:
    def __init__(self, contract_type: ContractType, contract_media: str, contract_nature: ContractNature, contract_owner: str):
        self.contract_type = contract_type
        self.contract_media = contract_media
        self.contract_nature = contract_nature
        self.contract_owner = contract_owner
