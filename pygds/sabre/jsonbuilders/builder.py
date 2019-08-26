from pygds.core.request import LowFareSearchRequest


class SabreBFMBuilder:
    """This class can generate JSON needed for sabre search flight requests."""

    def __init__(self, search_request: LowFareSearchRequest, target: str = "Production", AvailableFlightsOnly: bool = True):
        self.target = target
        self.AvailableFlightsOnly = True
        self.search_request: LowFareSearchRequest = search_request

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
                    "PseudoCityCode": self.search_request.pcc,
                    "ISOCountry": "US"
                }
            ]
        }

    def origin_destination_information(self):
        my_return = []
        itinaries = self.search_request.itineraries
        for i in itinaries:
            my_return.append(
                {
                    "TPA_Extensions": {
                        "SegmentType": {
                            "Code": "O"
                        },
                        "CabinPref": {
                            "Cabin": self.search_request.csv
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

    def _trip_type(self):
        itin_count = len(self.search_request.to_data().itineraries)
        print(self.search_request.to_data().itineraries)
        if itin_count == 1:
            return "OneWay"

        if itin_count == 2:
            if self.search_request.to_data().itineraries[0]["origin"] != self.search_request.to_data().itineraries[1]["destination"] or self.search_request.to_data().itineraries[0]["destination"] != self.search_request.to_data().itineraries[1]["origin"]:
                return "OpenJaw"
            return "Return"

        if self.search_request.search_request.to_data()[0]["origin"] == self.search_request.to_data()[itin_count - 1]["destination"]:
            return "Circle"

        return "Other"

    def _is_alternate_date(self):
        if self.search_request.requestType in ["AD1", "AD3", "AD7"]:
            return True
        return False

    def _flexible_fare(self, pax_quanty_pub, pax_quanty_net, cabin, baggage_pref):
        return {
            "FlexibleFares": {
                "FareParameters": [
                    {
                        "PassengerTypeQuantity": pax_quanty_pub,
                        "Cabin": {
                            "Type": cabin
                        },
                        "NegotiatedFaresOnly": {
                            "Ind": True,
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
                        },
                        "Baggage": {
                            "FreePieceRequired": baggage_pref
                        }
                    },
                    {
                        "PassengerTypeQuantity": pax_quanty_net,
                        "Cabin": {
                            "Type": cabin
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
                        },
                        "Baggage": {
                            "FreePieceRequired": baggage_pref
                        }

                    }
                ]
            }
        }

    def travel_preferences(self):
        cabin = self.search_request.csv
        paxTypeQuantityPUB = []
        paxTypeQuantityPFA = []

        if self.search_request.adult != 0:
            paxTypeQuantityPUB.append({
                "Code": "ADT",
                "Quantity": self.search_request.adult

            })
            paxTypeQuantityPFA.append({
                "Code": "PFA",
                "Quantity": self.search_request.adult
            })

        if self.search_request.child != 0:
            paxTypeQuantityPUB.append({
                "Code": "CNN",
                "Quantity": self.search_request.child

            })
            paxTypeQuantityPFA.append({
                "Code": "CNN",
                "Quantity": self.search_request.child
            })

        if self.search_request.infant != 0:
            paxTypeQuantityPUB.append({
                "Code": "INF",
                "Quantity": self.search_request.infant

            })
            paxTypeQuantityPFA.append({
                "Code": "INF",
                "Quantity": self.search_request.infant
            })

        tpa_ext = {
            "LongConnectTime": {
                "Enable": True
            },
            "ExcludeVendorPref": [
                {
                    "Code": "WN"
                }
            ],
            "TripType": {
                "Value": self._trip_type()
            },
            "ExemptAllTaxes": {
                "Value": False
            },
            "ExemptAllTaxesAndFees": {
                "Value": False
            },
            "FlightStopsAsConnections": {
                "Ind": True
            },
            "JumpCabinLogic": {
                "Disabled": False
            },
            "DiversityParameters": {
                "Weightings": {
                    "PriceWeight": 10,
                    "TravelTimeWeight": 0
                },
                "AdditionalNonStopsPercentage": 100
            }
        }
        flexi_fare = dict()
        if self._is_alternate_date() is False:
            flexi_fare = self._flexible_fare(paxTypeQuantityPUB, paxTypeQuantityPFA, cabin, self.search_request.baggagePref)

        d = dict()

        """
        if self.search_request.excludeBasicEconomy == True:
            d = {"FareType": [
                {
                    "Code": "EOU",
                    "PreferLevel": "Unacceptable"
                },
                {
                    "Code": "ERU",
                    "PreferLevel": "Unacceptable"
                }
            ]}

        """
        tpa_ext = {**tpa_ext, **flexi_fare, **d}
        return {
            "ValidInterlineTicket": True,
            "FlightTypePref": {
                "MaxConnections": str(self.search_request.maxConnection)
            },
            "TPA_Extensions": tpa_ext,
            "AncillaryFees": {
                "Enable": True,
                "Summary": True,
                "AncillaryFeeGroup": [
                    {
                        "Code": "BG",
                        "Count": "3"
                    }
                ]
            },
            "VendorPref": [vend for vend in self.search_request.preferredAirlines]
        }

    def travel_info_summary(self, types):

        paxTypeQuantity = []

        if self.search_request.adult != 0:
            paxTypeQuantity.append({
                "type": "ADT" if types == "PUB" else "JCB",
                "quantity": self.search_request.adult
            }
            )
        if self.search_request.child != 0:
            paxTypeQuantity.append({
                "type": "CNN" if types == "PUB" else "JNN",
                "quantity": self.search_request.child
            }
            )

        if self.search_request.infant != 0:
            paxTypeQuantity.append({
                "type": "INF" if types == "PUB" else "JNF",
                "quantity": self.search_request.infant
            }
            )

        pf = {
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
                        "Ind": True
                    }
                },
                "BrandedFareIndicators": {
                    "SingleBrandedFare": True,
                    "MultipleBrandedFares": False
                }
            },
            "NegotiatedFaresOnly": False
        }

        account_list = dict()
        if self._is_alternate_date() and types == "COM":
            account_list = {
                "AccountCode": [{"Code": "COM"}]
            }

        pf = {**pf, **account_list}
        print(pf)

        return {"AirTravelerAvail": [
                {
                    "PassengerTypeQuantity": [{"Code": el["type"], "Quantity": el["quantity"], "TPA_Extensions": {
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
                    }} for el in paxTypeQuantity],

                }],
                "PriceRequestInformation": pf
                }

    def tpa_extensions(self):
        return {
            "IntelliSellTransaction": {
                "RequestType": {
                    "Name": self.search_request.requestType
                },
                "CompressResponse": {
                    "Value": True
                }
            },
            "AlternatePCC": [i for i in self.search_request.alternatePcc]
        }

    def search_flight(self, types):
        return {
            "OTA_AirLowFareSearchRQ": {
                "POS": self.pos(),
                "OriginDestinationInformation": self.origin_destination_information(),
                "TravelPreferences": self.travel_preferences(),
                "TravelerInfoSummary": self.travel_info_summary(types),
                "TPA_Extensions": self.tpa_extensions(),
                "Target": "Production",
                "Version": "4.1.0",
                "AvailableFlightsOnly": True
            }
        }
