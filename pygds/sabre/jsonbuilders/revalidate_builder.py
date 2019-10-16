from .revalidate import Itineraries, FlightSegment


class RevalidateBuilder:
    """This class can generate JSON needed for sabre search flight requests."""

    def __init__(self, pcc, itineraries: list = [], passengers: list = [], fare_type: str = "", target: str = ""):
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
        list_itineraries = []
        for itin_index, itin in enumerate(self.itineraries):
            list_segments = []
            for seg in itin.segments:
                flight = FlightSegment()
                flight.flight_number = int(seg.flight_number)
                flight.departure_date_time = seg.departure_date_time
                flight.arrival_date_time = seg.arrival_date_time
                flight.res_book_desig_code = seg.res_book_desig_code
                flight.origin_location = seg.departure_airport.airport
                flight.destination_location = seg.arrival_airpot.airport
                flight.marketing_airline = seg.marketing.airline_code
                flight.operating_airline = seg.operating.airline_code
                list_segments.append(flight.to_dict())
            origin = itin.segments[0].departure_airport.airport
            destination = itin.segments[-1].arrival_airpot.airport
            departure_date = itin.segments[0].departure_date_time
            itinerary = Itineraries(str(itin_index + 1), origin, destination, departure_date, list_segments).to_dict()
            list_itineraries.append(itinerary)

        return list_itineraries

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
