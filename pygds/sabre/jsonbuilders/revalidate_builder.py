from .revalidate import Itineraries
from typing import List


class RevalidateBuilder:
    """This class can generate JSON needed for sabre search flight requests."""

    def __init__(self, pcc, itineraries: List[Itineraries], passengers: list = [], fare_type: str = "", target: str = ""):
        self.pcc = pcc
        self.itineraries = itineraries
        self.passengers = passengers
        self.fare_type = fare_type
        self.target = target
        self.list_adult = ["ADT", "JCB"]
        self.list_child = ["CNN", "JNN", "J12", "J11", "J10", "J09", "J08", "J07", "J06", "J05", "J04", "J03", "J02", "C12", "C11", "C10", "C09", "C08", "C07", "C06", "C05", "C04", "C03", "C02"]

    def pos(self):
        return {
            "Source": [
                {
                    "RequestorID": {
                        "CompanyName": {
                            "Code": "TN"
                        },
                        "Type": "1",
                        "ID": "1"
                    },
                    "PseudoCityCode": self.pcc
                }
            ]
        }

    def origin_destination_information(self):
        return self.itineraries

    def get_tpa_extension(self):
        return {
            "VoluntaryChanges": {
                "Match": "Info",
                "Penalty": [
                    {
                        "Type": "Refund"
                    },
                    {
                        "Type": "Exchange"
                    }
                ]
            }
        }

    def all_passengers(self):
        list_passengers = []
        for pax in self.passengers:
            if self.fare_type == "Pub":
                if pax['code'] in self.list_adult:
                    list_passengers.append({
                        "Code": "ADT",
                        "Quantity": pax['quantity'],
                        "TPA_Extensions": self.get_tpa_extension()
                    })

                elif pax['code'] in self.list_child:
                    list_passengers.append({
                        "Code": "C" + str(pax['code'][-2:]),
                        "Quantity": pax['quantity'],
                        "TPA_Extensions": self.get_tpa_extension()
                    })

                else:
                    list_passengers.append({
                        "Code": "INF",
                        "Quantity": pax['quantity'],
                        "TPA_Extensions": self.get_tpa_extension()
                    })

            elif self.fare_type == "Net":
                if pax['code'] in self.list_adult:
                    list_passengers.append({
                        "Code": "JCB",
                        "Quantity": pax['quantity'],
                        "TPA_Extensions": self.get_tpa_extension()
                    })

                elif pax['code'] in self.list_child:
                    list_passengers.append({
                        "Code": "J" + str(pax['code'][-2:]),
                        "Quantity": pax['quantity'],
                        "TPA_Extensions": self.get_tpa_extension()
                    })

                else:
                    list_passengers.append({
                        "Code": "JNF",
                        "Quantity": pax['quantity'],
                        "TPA_Extensions": self.get_tpa_extension()
                    })

        return list_passengers

    def flight(self, segment):
        return {
            "Number": int(segment["flight_number"]),
            "DepartureDateTime": segment["departure_date"],
            "ArrivalDateTime": segment["arrival_date"],
            "Type": segment["type_flight"],
            "ClassOfService": segment["class_of_service"],
            "OriginLocation": {
                "LocationCode": segment["origin"]
            },
            "DestinationLocation": {
                "LocationCode": segment["destination"]
            },
            "Airline": {
                "Operating": segment["operating"],
                "Marketing": segment["marketing"]
            }
        }

    def traveler_info_summary(self):
        return {
            "AirTravelerAvail": [
                {
                    "PassengerTypeQuantity": self.all_passengers()
                }
            ],
            "PriceRequestInformation": {
                "TPA_Extensions": {
                    "BrandedFareIndicators": {
                        "MultipleBrandedFares": True,
                        "ReturnBrandAncillaries": True
                    }
                }
            }
        }

    def travel_preference(self):
        return {
            "ETicketDesired": True,
            "ValidInterlineTicket": True,
            "MaxStopsQuantity": 2,
            "TPA_Extensions": {
                "VerificationItinCallLogic": {
                    "Value": "B"
                }
            }
        }
