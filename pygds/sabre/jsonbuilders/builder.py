

class SabreBFMBuilder:
    """This class can generate JSON needed for sabre search flight requests."""

    def __init__(self, search_request="", target: str = "Production", AvailableFlightsOnly: bool = True):
        self.target = target
        self.AvailableFlightsOnly = True
        self.search_request = search_request

    def pos(self):
        return {
            "Source": [
                {
                    "RequestorID": {
                        "CompanyName": {
                            "Code": "TN",
                            "content": "Context"
                        },
                        "URL": "http://www.sabre.com/",
                        "Type": "1",
                        "ID": "1"
                    },
                    "PseudoCityCode": self.search_request["pcc"],
                    "ISOCountry": "US"
                }
            ]
        }

    def origin_destination_information(self):
        my_return = []
        itinaries = self.search_request["itineraries"]
        for i in itinaries:
            my_return.append(
                {
                    "TPA_Extensions": {
                        "SegmentType": {
                            "Code": "O"
                        },
                        "CabinPref": {
                            "Cabin": self.search_request["csv"]
                        }
                    },
                    "RPH": str(itinaries.index(i) + 1),
                    "OriginLocation": {
                        "LocationCode": i["origin"],
                        "CodeContext": "IATA"
                    },
                    "DestinationLocation": {
                        "LocationCode": i["destination"],
                        "CodeContext": "IATA"
                    },
                    "DepartureDateTime": i["departureDate"] + "T11:00:00"
                }
            )
        return my_return

    def trip_type(self):
        itin_count = len(self.search_request["itineraries"])
        if itin_count == 1:
            return "OneWay"

        if itin_count == 2:
            if self.search_request["itineraries"][0]["origin"] != self.search_request["itineraries"][1]["destination"] or self.search_request["itineraries"][0]["destination"] != self.search_request["itineraries"][1]["origin"]:
                return "OpenJaw"
            return "Return"

        if self.search_request["itineraries"][0]["origin"] == self.search_request["itineraries"][itin_count - 1]["destination"]:
            return "Circle"

        return "Other"

    def travel_preferences(self):
        cabin = self.search_request["csv"]
        paxTypeQuantityPUB = []
        paxTypeQuantityPFA = []

        if self.search_request["adult"] != 0:
            paxTypeQuantityPUB.append({
                "Code": "ADT",
                "Quantity": self.search_request["adult"]

            })
            paxTypeQuantityPFA.append({
                "Code": "PFA",
                "Quantity": self.search_request["adult"]
            })

        if self.search_request["child"] != 0:
            paxTypeQuantityPUB.append({
                "Code": "CNN",
                "Quantity": self.search_request["child"]

            })
            paxTypeQuantityPFA.append({
                "Code": "CNN",
                "Quantity": self.search_request["child"]
            })

        if self.search_request["infant"] != 0:
            paxTypeQuantityPUB.append({
                "Code": "INF",
                "Quantity": self.search_request["infant"]

            })
            paxTypeQuantityPFA.append({
                "Code": "INF",
                "Quantity": self.search_request["infant"]
            })

        tpa_ext = {
            "LongConnectTime": {
                "Enable": str(True).lower()
            },
            "ExcludeVendorPref": [
                {
                    "Code": "WN"
                }
            ],
            "TripType": {
                "Value": self.trip_type()
            },
            "ExemptAllTaxes": {
                "Value": str(False).lower()
            },
            "ExemptAllTaxesAndFees": {
                "Value": str(False).lower()
            },
            "FlightStopsAsConnections": {
                "Ind": str(True).lower()
            },
            "JumpCabinLogic": {
                "Disabled": str(False).lower()
            },
            "DiversityParameters": {
                "Weightings": {
                    "PriceWeight": 10,
                    "TravelTimeWeight": 0
                },
                "AdditionalNonStopsPercentage": 100
            }
        }

        if self.search_request["excludeBasicEconomy"] == str(True).lower():
            tpa_ext = tpa_ext + "," + """FareType: [
                    {
                        "Code": "EOU",
                        "PreferLevel": "Unacceptable"
                    },
                    {
                        "Code": "ERU",
                        "PreferLevel": "Unacceptable"
                    }
                ]"""
        return  tpa_ext
    def travel_info_summary(self):
        pass

    def tpa_extensions(self):
        pass

    def search_flight(self):
        return  {
            "OTA_AirLowFareSearchRQ":{
                "POS":self.pos(),
                "OriginDestinationInformation": self.origin_destination_information(),
                "TravelPreferences": self.travel_preferences(),
                "TravelerInfoSummary": self.travel_info_summary(),
                "TPA_Extensions": self.tpa_extensions(),
                "Target": "Production",
                "Version": "4.1.0",
                "AvailableFlightsOnly": str(True).lower()
            }
        }

    def itinaries(self):
        return {
                    {
            "OTA_AirLowFareSearchRQ": {
            "POS" : SabreBFMBuilder().pos(),
            "OriginDestinationInformation": [
                {
                    "TPA_Extensions": {
                        "SegmentType": {
                            "Code": "O"
                        },
                        "CabinPref": {
                            "Cabin": "Y"
                        }
                    },
                    "RPH": "1",
                    "OriginLocation": {
                        "LocationCode": "DTW",
                        "CodeContext": "IATA"
                    },
                    "DestinationLocation": {
                        "LocationCode": "CDG",
                        "CodeContext": "IATA"
                    },
                    "DepartureDateTime": "2019-10-08T11:00:00"
                },
                {
                    "TPA_Extensions": {
                        "SegmentType": {
                            "Code": "O"
                        },
                        "CabinPref": {
                            "Cabin": "Y"
                        }
                    },
                    "RPH": "2",
                    "OriginLocation": {
                        "LocationCode": "CDG",
                        "CodeContext": "IATA"
                    },
                    "DestinationLocation": {
                        "LocationCode": "DTW",
                        "CodeContext": "IATA"
                    },
                    "DepartureDateTime": "2019-10-21T11:00:00"
                }
            ],
            "TravelPreferences": {
                "ValidInterlineTicket": true,
                "FlightTypePref": {
                    "MaxConnections": "2"
                },
                "TPA_Extensions": {
                    "LongConnectTime": {
                        "Enable": true
                    },
                    "ExcludeVendorPref": [
                        {
                            "Code": "WN"
                        }
                    ],
                    "TripType": {
                        "Value": "Return"
                    },
                    "ExemptAllTaxes": {
                        "Value": false
                    },
                    "ExemptAllTaxesAndFees": {
                        "Value": false
                    },
                    "FlightStopsAsConnections": {
                        "Ind": true
                    },
                    "JumpCabinLogic": {
                        "Disabled": false
                    },
                    "FlexibleFares": {
                        "FareParameters": [
                            {
                                "PassengerTypeQuantity": [
                                    {
                                        "Code": "JCB",
                                        "Quantity": 2
                                    },
                                    {
                                        "Code": "JNN",
                                        "Quantity": 1
                                    },
                                    {
                                        "Code": "JNF",
                                        "Quantity": 1
                                    }
                                ],
                                "Cabin": {
                                    "Type": "Y"
                                },
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
                            },
                            {
                                "PassengerTypeQuantity": [
                                    {
                                        "Code": "ADT",
                                        "Quantity": 2
                                    },
                                    {
                                        "Code": "CNN",
                                        "Quantity": 1
                                    },
                                    {
                                        "Code": "INF",
                                        "Quantity": 1
                                    }
                                ],
                                "Cabin": {
                                    "Type": "Y"
                                },
                                "NegotiatedFaresOnly": {
                                    "Ind": true
                                },
                                "AccountCode": [
                                    {
                                        "Code": "COM"
                                    }
                                ],
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
                            },
                            {
                                "PassengerTypeQuantity": [
                                    {
                                        "Code": "PFA",
                                        "Quantity": 2
                                    },
                                    {
                                        "Code": "CNN",
                                        "Quantity": 1
                                    },
                                    {
                                        "Code": "INF",
                                        "Quantity": 1
                                    }
                                ],
                                "Cabin": {
                                    "Type": "Y"
                                },
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
                            },
                            {
                                "PassengerTypeQuantity": [
                                    {
                                        "Code": "JCB",
                                        "Quantity": 2
                                    },
                                    {
                                        "Code": "JNN",
                                        "Quantity": 1
                                    },
                                    {
                                        "Code": "JNF",
                                        "Quantity": 1
                                    }
                                ],
                                "Cabin": {
                                    "Type": "S"
                                },
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
                            },
                            {
                                "PassengerTypeQuantity": [
                                    {
                                        "Code": "ADT",
                                        "Quantity": 2
                                    },
                                    {
                                        "Code": "CNN",
                                        "Quantity": 1
                                    },
                                    {
                                        "Code": "INF",
                                        "Quantity": 1
                                    }
                                ],
                                "Cabin": {
                                    "Type": "S"
                                },
                                "NegotiatedFaresOnly": {
                                    "Ind": true
                                },
                                "AccountCode": [
                                    {
                                        "Code": "COM"
                                    }
                                ],
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
                            },
                            {
                                "PassengerTypeQuantity": [
                                    {
                                        "Code": "PFA",
                                        "Quantity": 2
                                    },
                                    {
                                        "Code": "CNN",
                                        "Quantity": 1
                                    },
                                    {
                                        "Code": "INF",
                                        "Quantity": 1
                                    }
                                ],
                                "Cabin": {
                                    "Type": "S"
                                },
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
                        ]
                    },
                    "DiversityParameters": {
                        "Weightings": {
                            "PriceWeight": 10,
                            "TravelTimeWeight": 0
                        },
                        "AdditionalNonStopsPercentage": 100
                    }
                },
                "AncillaryFees": {
                    "Enable": true,
                    "Summary": true,
                    "AncillaryFeeGroup": [
                        {
                            "Code": "BG",
                            "Count": "3"
                        }
                    ]
                }
            },
            "TravelerInfoSummary": {
                "AirTravelerAvail": [
                    {
                        "PassengerTypeQuantity": [
                            {
                                "Code": "JCB",
                                "Quantity": 2,
                                "TPA_Extensions": {
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
                            },
                            {
                                "Code": "CNN",
                                "Quantity": 1,
                                "TPA_Extensions": {
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
                            },
                            {
                                "Code": "INF",
                                "Quantity": 1,
                                "TPA_Extensions": {
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
                            }
                        ]
                    }
                ],
                "PriceRequestInformation": {
                    "NegotiatedFareCode": [],
                    "TPA_Extensions": {
                        "Priority": {
                            "Price": {
                                "Priority": 1
                            },
                            "DirectFlights": {
                                "Priority": 4
                            },
                            "Time": {
                                "Priority": 2
                            },
                            "Vendor": {
                                "Priority": 3
                            }
                        },
                        "Indicators": {
                            "RefundPenalty": {
                                "Ind": true
                            }
                        },
                        "BrandedFareIndicators": {
                            "SingleBrandedFare": true,
                            "MultipleBrandedFares": false
                        }
                    },
                    "NegotiatedFaresOnly": false
                }
            },
            "TPA_Extensions": {
                "IntelliSellTransaction": {
                    "RequestType": {
                        "Name": "50ITINS"
                    },
                    "CompressResponse": {
                        "Value": true
                    }
                },
                "MultiTicket": {
                    "DisplayPolicy": "SOW"
                },
                "AlternatePCC": []
            },
            "Target": "Production",
            "Version": "4.1.0",
            "AvailableFlightsOnly": true
            }
        }
        }

    def traveler_info_summary(self):
        pass

    def tpa_Extensions(self):
        pass
