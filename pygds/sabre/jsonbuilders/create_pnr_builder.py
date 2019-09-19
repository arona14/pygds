from .create_pnr import CreatePnrRequest
from pygds.core.helpers import reformat_date


class CreatePnrBuilder:

    def __init__(self, create_pnr_request: CreatePnrRequest):
        self.create_pnr_request = create_pnr_request
        self.version: str = "2.1.0"
        self.net_pax_types: list = ["JCB", "JNN", "JNF"]
        self.infant_pax_types: list = ["JNF", "INF"]

    def air_price(self):
        price_request_info = []
        for pax in self.create_pnr_request.passengers:
            if len(self.create_pnr_request.passengers) == 1:
                pricing_qualifiers = {
                    "PassengerType": [
                        {
                            "Code": pax.passenger_type,
                            "Quantity": "1"
                        }
                    ]
                }
            else:
                pricing_qualifiers = {
                    "NameSelect": [
                        {
                            "NameNumber": str(pax.name_number) + ".1"
                        }
                    ],
                    "PassengerType": [
                        {
                            "Code": pax.passenger_type,
                            "Quantity": "1"
                        }
                    ],
                }
            misc_qualifiers = {
                "AirExtras": {
                    "Ind": True
                },
                "Commission": {}
            }
            if pax.passenger_type.startswith("J"):
                misc_qualifiers["Commission"]["Amount"] = str(pax.amount)
                if pax.amount:
                    pricing_qualifiers["PlusUp"] = {"Amount": str(pax.amount)}
            else:
                misc_qualifiers["Commission"]["Percent"] = "0"
            if self.create_pnr_request.fare_type == 'COM':
                misc_qualifiers["Commission"]["Percent"] = str(self.create_pnr_request.commission)
                if pax.tour_code and pax.passenger_type in self.infant_pax_types:
                    misc_qualifiers["TourCode"]["Percent"] = {
                        "SuppressIT": {
                            "Ind": True
                        },
                        "Text": pax.tour_code
                    }
                if pax.ticket_designator and pax.passenger_type in self.infant_pax_types:
                    pricing_qualifiers["CommandPricing"] = [
                        {
                            "Discount": "0",
                            "AuthCode": self.create_pnr_request.ticket_designator
                        }
                    ]
            price_request_info.append(
                {
                    "PriceRequestInformation": {
                        "Retain": True,
                        "OptionalQualifiers": {
                            "MiscQualifiers": misc_qualifiers,
                            "PricingQualifiers": pricing_qualifiers
                        }
                    }
                })
        return price_request_info

    def flight_segment(self):
        segments = []
        infant_count = 0
        for pax in self.create_pnr_request.passengers:
            if pax.passenger_type in self.infant_pax_types:
                infant_count += 1
        for segment in self.create_pnr_request.flight_segments:
            seg = {
                "ArrivalDateTime": segment.arrival_date_time,
                "DepartureDateTime": segment.departure_date_time,
                "FlightNumber": segment.flight_number,
                "NumberInParty": str(segment.number_in_party),
                "ResBookDesigCode": segment.res_book_desig_code,
                "Status": 'NN',
                "DestinationLocation": {
                    "LocationCode": segment.destination_location
                },
                "MarketingAirline": {
                    "Code": segment.marketing_airline,
                    "FlightNumber": segment.flight_number
                },
                "MarriageGrp": segment.marriage_grp,
                "OperatingAirline": {
                    "Code": segment.operating_airline
                },
                "OriginLocation": {
                    "LocationCode": segment.origin_location
                }
            }
            segments.append(seg)
        return segments

    def air_book(self):
        return {
            "HaltOnStatus": [
                {
                    "Code": "NO"
                },
                {
                    "Code": "NN"
                },
                {
                    "Code": "UC"
                },
                {
                    "Code": "US"
                }
            ],

            "OriginDestinationInformation": {
                "FlightSegment": self.flight_segment()
            },
            "RedisplayReservation": {
                "NumAttempts": 2,
                "WaitInterval": 2000
            },
            "RetryRebook": {
                "Option": True
            }
        }

    def post_processing(self):
        return {
            "EndTransaction": {
                "Source": {
                    "ReceivedFrom": "E"
                }
            },
            "RedisplayReservation": True,
            "UnmaskCreditCard": True
        }

    def secure_flight(self, passengers):
        return [
            {
                "PersonName": {
                    "GivenName": str(passenger.given_name) + " " + str(passenger.middle_name),
                    "NameNumber": "1.1" if passenger.passenger_type in self.infant_pax_types else str(passenger.name_number) + ".1",
                    "Surname": passenger.surname,
                    "Gender": self.get_gender(passenger),
                    "DateOfBirth": passenger.date_of_birth
                },
                "SegmentNumber": 'A'
            }
            for passenger in passengers
        ]

    def get_gender(self, pax):
        gender = "M" if pax.gender == "Male" else "F"
        if pax.passenger_type in self.infant_pax_types:
            gender = "MI" if pax.gender == "Male" else "FI"

        return gender

    def get_number_infant(self):
        infants_in_party = []
        for pax in self.create_pnr_request.passengers:
            if pax.passenger_type in self.infant_pax_types:
                infants_in_party.append(pax)

        return infants_in_party

    def sepecial_req_details(self):
        infants_in_party = self.get_number_infant()
        secure_flight = self.secure_flight(self.create_pnr_request.passengers)
        secure = {
            "SpecialService": {
                "SpecialServiceInfo": {
                    "SecureFlight": secure_flight,
                }
            },
            "AddRemark": {
                "RemarkInfo": {
                    "Remark": self.create_pnr_request.remarks
                }
            }
        }
        if len(infants_in_party) > 0:
            service = self.service(infants_in_party)
            secure["SpecialService"]["SpecialServiceInfo"]["Service"] = service
        return secure

    def service(self, infants_in_party):
        return [
            {
                "PersonName": {
                    "NameNumber": "1.1"
                },
                "Text": inf.surname.upper() + "/" + str(inf.given_name) + " " + str(inf.middle_name).upper() + "/" + reformat_date(inf.date_of_birth, "%Y-%m-%d", "%d%b%y"),
                "SegmentNumber": "A",
                "SSR_Code": "INFT"
            }
            for inf in infants_in_party
        ]

    def travel_itinerarry_add_info(self, pnr_request):
        info = {
            "AgencyInfo": {
                "Ticketing": {
                    "TicketType": "7TAW" + (reformat_date(pnr_request.last_ticket_date, "%Y-%m-%d", "%d%b%y")[0:-2]).upper() + "/1159P" if pnr_request.last_ticket_date else "7TAW"
                }
            },
            "CustomerInfo": {
                "ContactNumbers": {
                    "ContactNumber": [
                        {
                            "NameNumber": "1.1",
                            "Phone": pnr_request.passengers[0].phone if pnr_request.passengers[0].phone else "4567890",
                            "PhoneUseType": 'H'
                        }
                    ]
                },
                "CreditCardData": {
                    "PreferredCustomer": {
                        "ind": True
                    }
                },
                "CustomerIdentifier": str(pnr_request.customer_identifier),
                "PersonName": [{"GivenName": str(pax.given_name) + " " + str(pax.middle_name),
                                "Infant": True if pax.passenger_type in self.infant_pax_types else False,
                                "NameNumber": str(pax.name_number) + ".1",
                                "PassengerType": pax.passenger_type,
                                "Surname": pax.surname} for pax in self.create_pnr_request.passengers]
            }
        }
        if self.create_pnr_request.passengers[0].email:
            info["CustomerInfo"]["Email"] = [
                {
                    "Address": self.create_pnr_request.passengers[0].email
                }
            ]
        return info

    def to_dict(self):
        return {
            "CreatePassengerNameRecordRQ": {
                "AirBook": self.air_book(),
                "AirPrice": self.air_price(),
                "PostProcessing": self.post_processing(),
                "SpecialReqDetails": self.sepecial_req_details(),
                "TravelItineraryAddInfo": self.travel_itinerarry_add_info(self.create_pnr_request),
                "targetCity": self.create_pnr_request.target_city,
                "version": self.version
            }
        }
